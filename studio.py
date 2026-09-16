#!/usr/bin/env python3
"""
Studio — une page web locale pour monter tes videos en parlant a l'agent.

    python3 studio.py

Ouvre http://localhost:8765 dans ton navigateur. Tu glisses tes videos dans la
page, tu ecris ce que tu veux dans la barre du bas, l'agent monte, le resultat
s'affiche. Tu continues a lui parler pour corriger.

Tout reste sur ta machine : le serveur tourne en local, les fichiers ne
bougent pas de ce dossier, et le montage passe par le Claude Code deja
installe et connecte a ton compte.
"""

import html
import json
import mimetypes
import os
import re
import shutil
import subprocess
import sys
import threading
import time
import uuid
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

PORT = 8765
FOLDER = Path.cwd()

# Quel agent pilote le montage. Change-le avec la variable STUDIO_AGENT :
#     STUDIO_AGENT=codex python3 studio.py
#
# Chaque profil construit la ligne de commande complete, selon qu'on ouvre une
# conversation ou qu'on reprend la precedente. Les options passent avant le
# message : "codex exec [OPTIONS] [PROMPT]" refuse un drapeau place apres le
# prompt. Les outils pre-approuves evitent que l'agent s'arrete a chaque
# commande ffmpeg ; ils ne valent que dans ce dossier.
AGENTS = {
    "claude": {
        "bin": "claude",
        "args": lambda msg, cont: (["--continue"] if cont else [])
                + ["-p", msg, "--allowedTools", "Bash,Read,Write,Edit,Glob,Grep"],
    },
    "codex": {
        "bin": "codex",
        "args": lambda msg, cont: ["exec"] + (["resume", "--last"] if cont else [])
                + CODEX_FLAGS + [msg],
        # Les options de "codex exec" varient d'une version a l'autre. Si l'une
        # est refusee, on relance avec le strict minimum plutot que d'echouer.
        "fallback": lambda msg: ["exec", msg],
    },
}

AGENT_NAME = os.environ.get("STUDIO_AGENT", "claude").strip().lower()

# Options passees a "codex exec". Vide par defaut : selon la version, des
# drapeaux comme --full-auto ou --sandbox n'existent que sur la commande
# interactive. Mets-en ici si ta version en accepte :
#     STUDIO_CODEX_FLAGS="--sandbox workspace-write" STUDIO_AGENT=codex python3 studio.py
CODEX_FLAGS = os.environ.get("STUDIO_CODEX_FLAGS", "").split()

# Variables qui detournent l'agent vers une cle d'API ou un proxy au lieu de ta
# session Claude. On les retire avant de le lancer, sans toucher a ton shell.
AUTH_OVERRIDES = ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_BASE_URL")

VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm", ".mkv"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
MEDIA_EXT = VIDEO_EXT | IMAGE_EXT

JOBS = {}
JOBS_LOCK = threading.Lock()
STARTED_CONVERSATION = threading.Event()


# ---------------------------------------------------------------------------
# L'agent
# ---------------------------------------------------------------------------

def agent_profile():
    profile = AGENTS.get(AGENT_NAME)
    if profile is None:
        sys.exit("Agent inconnu : %s. Choix possibles : %s"
                 % (AGENT_NAME, ", ".join(sorted(AGENTS))))
    return profile


def agent_binary():
    profile = agent_profile()
    found = shutil.which(profile["bin"])
    if not found:
        hint = {
            "claude": "npm install -g @anthropic-ai/claude-code",
            "codex": "npm install -g @openai/codex",
        }.get(AGENT_NAME, "")
        sys.exit("'%s' est introuvable.\n  %s\n" % (profile["bin"], hint))
    return found


def run_agent(job_id, message):
    """Lance l'agent sur le message et accumule sa sortie dans le job."""
    profile = agent_profile()
    env = {k: v for k, v in os.environ.items() if k not in AUTH_OVERRIDES}

    def append(text):
        with JOBS_LOCK:
            JOBS[job_id]["output"] += text

    def launch(cont):
        return launch_cmd([agent_binary()] + profile["args"](message, cont))

    def launch_cmd(cmd):
        try:
            proc = subprocess.Popen(
                cmd, cwd=str(FOLDER), stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, text=True, bufsize=1, env=env,
            )
        except OSError as exc:
            append("Impossible de lancer l'agent : %s\n" % exc)
            return None, ""
        captured = ""
        for line in proc.stdout:
            captured += line
            append(line)
        proc.wait()
        return proc.returncode, captured

    cont = STARTED_CONVERSATION.is_set()
    code, out = launch(cont)

    # Un argument a ete refuse (reprise non supportee, drapeau inconnu de cette
    # version) : on relance avec le strict minimum au lieu de rendre la main
    # sur une erreur d'outil.
    refused = ("unexpected argument" in out or "unrecognized" in out
               or "unknown option" in out)
    fallback = profile.get("fallback")
    if code not in (0, None) and refused and fallback:
        append("\n[argument refuse — relance sans options]\n")
        code, out = launch_cmd([agent_binary()] + fallback(message))

    STARTED_CONVERSATION.set()
    with JOBS_LOCK:
        JOBS[job_id]["status"] = "fini" if code == 0 else "erreur"
        JOBS[job_id]["code"] = code


# ---------------------------------------------------------------------------
# Le dossier
# ---------------------------------------------------------------------------

def list_media():
    """Tous les medias du dossier, les plus recents en premier."""
    items = []
    for path in FOLDER.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in MEDIA_EXT:
            continue
        if any(part.startswith(".") for part in path.parts):
            continue
        rel = path.relative_to(FOLDER)
        items.append({
            "path": str(rel),
            "name": path.name,
            "kind": "video" if path.suffix.lower() in VIDEO_EXT else "image",
            "size": path.stat().st_size,
            "mtime": path.stat().st_mtime,
        })
    items.sort(key=lambda i: i["mtime"], reverse=True)
    return items


def safe_path(rel):
    """Empeche de sortir du dossier via ../"""
    target = (FOLDER / unquote(rel)).resolve()
    if not str(target).startswith(str(FOLDER.resolve())):
        return None
    return target if target.is_file() else None


# ---------------------------------------------------------------------------
# Le serveur
# ---------------------------------------------------------------------------

class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *args):
        pass

    # -- reponses ----------------------------------------------------------

    def send_json(self, payload, code=200):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, markup):
        body = markup.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_media(self, path):
        """Sert un fichier, avec support des plages pour la lecture video."""
        size = path.stat().st_size
        ctype = mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        rng = self.headers.get("Range")

        start, end = 0, size - 1
        partial = False
        if rng:
            match = re.match(r"bytes=(\d*)-(\d*)", rng)
            if match:
                if match.group(1):
                    start = int(match.group(1))
                if match.group(2):
                    end = min(int(match.group(2)), size - 1)
                partial = True

        length = max(0, end - start + 1)
        self.send_response(206 if partial else 200)
        self.send_header("Content-Type", ctype)
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Content-Length", str(length))
        if partial:
            self.send_header("Content-Range", "bytes %d-%d/%d" % (start, end, size))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()

        with path.open("rb") as handle:
            handle.seek(start)
            remaining = length
            while remaining > 0:
                chunk = handle.read(min(65536, remaining))
                if not chunk:
                    break
                try:
                    self.wfile.write(chunk)
                except (BrokenPipeError, ConnectionResetError):
                    return
                remaining -= len(chunk)

    # -- routes ------------------------------------------------------------

    def do_GET(self):
        route = urlparse(self.path).path

        if route == "/":
            return self.send_html(PAGE)

        if route == "/api/files":
            return self.send_json({"files": list_media()})

        if route.startswith("/api/job/"):
            job_id = route[len("/api/job/"):]
            with JOBS_LOCK:
                job = JOBS.get(job_id)
                payload = dict(job) if job else None
            if payload is None:
                return self.send_json({"erreur": "job inconnu"}, 404)
            return self.send_json(payload)

        if route.startswith("/media/"):
            path = safe_path(route[len("/media/"):])
            if not path:
                return self.send_json({"erreur": "introuvable"}, 404)
            return self.send_media(path)

        self.send_json({"erreur": "route inconnue"}, 404)

    def do_POST(self):
        route = urlparse(self.path).path
        length = int(self.headers.get("Content-Length") or 0)

        if route == "/api/upload":
            name = unquote(self.headers.get("X-Filename", "")).strip()
            name = os.path.basename(name)
            if not name:
                return self.send_json({"erreur": "nom de fichier manquant"}, 400)
            target = FOLDER / name
            with target.open("wb") as handle:
                remaining = length
                while remaining > 0:
                    chunk = self.rfile.read(min(1 << 20, remaining))
                    if not chunk:
                        break
                    handle.write(chunk)
                    remaining -= len(chunk)
            return self.send_json({"ok": True, "nom": name})

        if route == "/api/chat":
            try:
                data = json.loads(self.rfile.read(length) or b"{}")
            except ValueError:
                return self.send_json({"erreur": "requete illisible"}, 400)
            message = (data.get("message") or "").strip()
            if not message:
                return self.send_json({"erreur": "message vide"}, 400)

            job_id = uuid.uuid4().hex[:12]
            with JOBS_LOCK:
                JOBS[job_id] = {"status": "en cours", "output": "",
                                "message": message, "debut": time.time()}
            threading.Thread(target=run_agent, args=(job_id, message),
                             daemon=True).start()
            return self.send_json({"job": job_id})

        self.send_json({"erreur": "route inconnue"}, 404)


# ---------------------------------------------------------------------------
# La page
# ---------------------------------------------------------------------------

PAGE = r"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Studio</title>
<style>
:root{
  --bg:#0d1015; --panel:#151a21; --panel-2:#1c232c; --line:#262f3a;
  --ink:#e8ecf2; --dim:#8c97a6; --accent:#d9a441; --ok:#4ba36a; --bad:#d2635a;
}
*{box-sizing:border-box}
html,body{height:100%}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
  display:flex; flex-direction:column;
}
header{
  padding:12px 18px; border-bottom:1px solid var(--line);
  display:flex; align-items:center; gap:14px; flex:none;
}
header h1{font-size:15px; margin:0; letter-spacing:.14em; text-transform:uppercase; color:var(--accent)}
header .dir{font:12px ui-monospace,monospace; color:var(--dim)}
header .spacer{flex:1}
button{
  font:inherit; font-size:13px; border:1px solid var(--line); background:var(--panel-2);
  color:var(--ink); border-radius:4px; padding:6px 12px; cursor:pointer;
}
button:hover{border-color:var(--accent); color:var(--accent)}
button:disabled{opacity:.45; cursor:default}

main{flex:1; display:flex; min-height:0}
#side{
  width:260px; flex:none; border-right:1px solid var(--line);
  overflow-y:auto; padding:14px; background:var(--panel);
}
#side h2{font-size:11px; letter-spacing:.14em; text-transform:uppercase; color:var(--dim); margin:0 0 10px}
.file{
  display:flex; align-items:center; gap:9px; padding:7px 8px; border-radius:4px;
  cursor:pointer; font-size:13px; word-break:break-all;
}
.file:hover{background:var(--panel-2)}
.file.on{background:var(--panel-2); box-shadow:inset 2px 0 0 var(--accent)}
.file .tag{
  font:10px ui-monospace,monospace; color:var(--dim); border:1px solid var(--line);
  border-radius:3px; padding:1px 4px; flex:none;
}
.empty{color:var(--dim); font-size:13px; padding:8px}

#center{flex:1; display:flex; flex-direction:column; min-width:0}
#stage{
  flex:none; padding:16px; display:flex; justify-content:center;
  background:#07090c; border-bottom:1px solid var(--line); min-height:220px;
}
#stage video,#stage img{max-height:44vh; max-width:100%; border-radius:6px; background:#000}
#stage .none{color:var(--dim); font-size:13px; align-self:center}

#log{flex:1; overflow-y:auto; padding:16px; min-height:0}
.turn{margin-bottom:18px}
.turn .who{
  font-size:11px; letter-spacing:.12em; text-transform:uppercase;
  color:var(--dim); margin-bottom:5px;
}
.turn.me .who{color:var(--accent)}
.turn .body{
  white-space:pre-wrap; word-break:break-word; background:var(--panel);
  border:1px solid var(--line); border-radius:6px; padding:11px 13px;
  font:13px/1.55 ui-monospace,SFMono-Regular,monospace;
}
.turn.me .body{background:var(--panel-2); font-family:inherit; font-size:14.5px}
.state{font-size:12px; color:var(--dim); margin-top:6px}
.state.ok{color:var(--ok)} .state.bad{color:var(--bad)}
#hint{color:var(--dim); font-size:13.5px; max-width:52ch; line-height:1.7}
#hint b{color:var(--ink); font-weight:600}
#hint code{
  font:12.5px ui-monospace,monospace; background:var(--panel-2);
  border:1px solid var(--line); border-radius:3px; padding:1px 5px; color:var(--accent);
}
#hint ul{padding-left:18px; margin:10px 0 0}
#hint li{margin-bottom:5px}

#bar{
  flex:none; border-top:1px solid var(--line); padding:12px 16px;
  display:flex; gap:10px; align-items:flex-end; background:var(--panel);
}
#prompt{
  flex:1; resize:none; background:var(--panel-2); color:var(--ink);
  border:1px solid var(--line); border-radius:6px; padding:10px 12px;
  font:inherit; font-size:14.5px; max-height:180px;
}
#prompt:focus{outline:none; border-color:var(--accent)}
#send{padding:10px 18px; font-weight:600}

#drop{
  position:fixed; inset:0; background:rgba(13,16,21,.94); display:none;
  align-items:center; justify-content:center; font-size:20px; color:var(--accent);
  border:3px dashed var(--accent); z-index:9;
}
#drop.on{display:flex}
@media (max-width:760px){ #side{display:none} }
</style>
</head>
<body>

<header>
  <h1>Studio</h1>
  <span class="dir" id="dir"></span>
  <span class="spacer"></span>
  <button id="refresh">Rafraîchir</button>
</header>

<main>
  <aside id="side">
    <h2>Fichiers</h2>
    <div id="files"><p class="empty">Chargement…</p></div>
  </aside>

  <section id="center">
    <div id="stage"><span class="none">Glisse une vidéo dans la page</span></div>
    <div id="log"><div id="hint">
      <b>Glisse tes fichiers dans la page</b>, puis écris ce que tu veux dans la barre du bas.
      <ul>
        <li><code>Monte brut.mp4, mes captures sont dans broll/, sors-moi jour002.mp4</code></li>
        <li><code>Les sous-titres sont trop bas, monte-les de 10 %</code></li>
        <li><code>Analyse ref.mp4 et applique son style à ma vidéo</code></li>
      </ul>
      L'agent lit <code>CLAUDE.md</code> — pas besoin de répéter tes préférences.
      <b>Cmd+Entrée</b> pour envoyer.
    </div></div>
    <div id="bar">
      <textarea id="prompt" rows="2" placeholder="Monte brut.mp4, mes captures sont dans broll/, sors-moi jour002.mp4"></textarea>
      <button id="send">Envoyer</button>
    </div>
  </section>
</main>

<div id="drop">Lâche tes fichiers ici</div>

<script>
(function(){
  "use strict";
  var filesEl=document.getElementById("files"),
      stage=document.getElementById("stage"),
      log=document.getElementById("log"),
      prompt=document.getElementById("prompt"),
      send=document.getElementById("send"),
      drop=document.getElementById("drop"),
      refresh=document.getElementById("refresh"),
      dir=document.getElementById("dir");

  var current=null, busy=false;

  function human(n){
    if(n<1024) return n+" o";
    if(n<1048576) return (n/1024).toFixed(0)+" Ko";
    return (n/1048576).toFixed(1)+" Mo";
  }

  function show(file){
    current=file.path;
    stage.textContent="";
    var el;
    if(file.kind==="video"){
      el=document.createElement("video");
      el.controls=true; el.playsInline=true;
    } else {
      el=document.createElement("img");
      el.alt=file.name;
    }
    el.src="/media/"+encodeURI(file.path)+"?t="+Date.now();
    stage.appendChild(el);
    paintFiles(lastFiles);
  }

  var lastFiles=[];
  function paintFiles(list){
    lastFiles=list;
    filesEl.textContent="";
    if(!list.length){
      var p=document.createElement("p");
      p.className="empty";
      p.textContent="Aucun média dans le dossier.";
      filesEl.appendChild(p);
      return;
    }
    list.forEach(function(f){
      var row=document.createElement("div");
      row.className="file"+(f.path===current?" on":"");
      var tag=document.createElement("span");
      tag.className="tag";
      tag.textContent=f.kind==="video"?"VID":"IMG";
      var name=document.createElement("span");
      name.textContent=f.path;
      var size=document.createElement("span");
      size.className="tag";
      size.textContent=human(f.size);
      row.appendChild(tag); row.appendChild(name); row.appendChild(size);
      row.addEventListener("click", function(){ show(f); });
      filesEl.appendChild(row);
    });
  }

  function loadFiles(auto){
    return fetch("/api/files").then(function(r){return r.json();}).then(function(d){
      paintFiles(d.files);
      if(auto && d.files.length){
        var newest=d.files.filter(function(f){return f.kind==="video";})[0];
        if(newest) show(newest);
      }
      return d.files;
    });
  }

  function turn(who, cls){
    var hint=document.getElementById("hint");
    if(hint) hint.remove();
    var wrap=document.createElement("div");
    wrap.className="turn "+(cls||"");
    var w=document.createElement("div");
    w.className="who"; w.textContent=who;
    var b=document.createElement("div");
    b.className="body";
    wrap.appendChild(w); wrap.appendChild(b);
    log.appendChild(wrap);
    log.scrollTop=log.scrollHeight;
    return {wrap:wrap, body:b};
  }

  function submit(){
    var text=prompt.value.trim();
    if(!text || busy) return;
    busy=true; send.disabled=true;
    prompt.value="";

    turn("Toi","me").body.textContent=text;
    var t=turn("Agent");
    t.body.textContent="…";
    var state=document.createElement("div");
    state.className="state";
    state.textContent="L'agent travaille.";
    t.wrap.appendChild(state);

    fetch("/api/chat",{
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({message:text})
    }).then(function(r){return r.json();}).then(function(d){
      if(d.erreur) throw new Error(d.erreur);
      poll(d.job, t.body, state);
    }).catch(function(e){
      t.body.textContent="Erreur : "+e.message;
      state.className="state bad"; state.textContent="Échec.";
      busy=false; send.disabled=false;
    });
  }

  function poll(job, body, state){
    var started=Date.now();
    var timer=setInterval(function(){
      fetch("/api/job/"+job).then(function(r){return r.json();}).then(function(d){
        if(d.output) { body.textContent=d.output; log.scrollTop=log.scrollHeight; }
        var secs=Math.round((Date.now()-started)/1000);
        if(d.status==="en cours"){
          state.textContent="L'agent travaille — "+secs+" s";
          return;
        }
        clearInterval(timer);
        busy=false; send.disabled=false;
        if(d.status==="fini"){
          state.className="state ok";
          state.textContent="Fini en "+secs+" s";
        } else {
          state.className="state bad";
          state.textContent="Arrêté après "+secs+" s";
        }
        loadFiles(true);
      }).catch(function(){});
    }, 1500);
  }

  function upload(file){
    var t=turn("Envoi","me");
    t.body.textContent="Téléversement de "+file.name+"…";
    return fetch("/api/upload",{
      method:"POST",
      headers:{"X-Filename":encodeURIComponent(file.name)},
      body:file
    }).then(function(r){return r.json();}).then(function(){
      t.body.textContent=file.name+" est dans le dossier.";
      return loadFiles(false);
    });
  }

  send.addEventListener("click", submit);
  prompt.addEventListener("keydown", function(e){
    if(e.key==="Enter" && (e.metaKey||e.ctrlKey)){ e.preventDefault(); submit(); }
  });
  refresh.addEventListener("click", function(){ loadFiles(false); });

  var depth=0;
  window.addEventListener("dragenter", function(e){ e.preventDefault(); depth++; drop.classList.add("on"); });
  window.addEventListener("dragover", function(e){ e.preventDefault(); });
  window.addEventListener("dragleave", function(){ depth--; if(depth<=0){ depth=0; drop.classList.remove("on"); } });
  window.addEventListener("drop", function(e){
    e.preventDefault(); depth=0; drop.classList.remove("on");
    var list=Array.prototype.slice.call(e.dataTransfer.files);
    (function next(){
      if(!list.length) return;
      upload(list.shift()).then(next);
    })();
  });

  fetch("/api/files").then(function(r){return r.json();}).then(function(d){
    paintFiles(d.files);
    var v=d.files.filter(function(f){return f.kind==="video";})[0];
    if(v) show(v);
  });
})();
</script>
</body>
</html>
"""


# ---------------------------------------------------------------------------

def open_server():
    """Prend le premier port libre a partir de PORT, plutot que d'echouer."""
    last = None
    for port in range(PORT, PORT + 12):
        try:
            return ThreadingHTTPServer(("127.0.0.1", port), Handler), port
        except OSError as exc:
            last = exc
            continue
    sys.exit(
        "Aucun port libre entre %d et %d.\n"
        "  Un studio tourne deja ? Ferme-le, ou libere le port :\n"
        "    lsof -ti :%d | xargs kill\n"
        "  (%s)\n" % (PORT, PORT + 11, PORT, last)
    )


def main():
    agent_binary()
    server, port = open_server()
    url = "http://localhost:%d" % port
    print("\n  Studio\n")
    print("  Agent   : %s" % AGENT_NAME)
    print("  Dossier : %s" % FOLDER)
    print("  Adresse : %s%s" % (url, "" if port == PORT else
          "   (le port %d etait pris)" % PORT))
    stripped = [k for k in AUTH_OVERRIDES if k in os.environ]
    if stripped:
        print("  Ignore  : %s (l'agent utilise ta session, pas une cle d'API)"
              % ", ".join(stripped))
    print("\n  Ctrl+C pour arreter.\n")
    threading.Timer(1.0, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Arrete.\n")
        server.server_close()


if __name__ == "__main__":
    main()
