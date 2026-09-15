#!/usr/bin/env python3
"""
Monteur automatique pour les vidéos quotidiennes du MBA de fondateur.

Tu donnes : une vidéo brute + un dossier de B-roll.
Tu reçois  : une vidéo verticale montée, coupée, sous-titrée.

    python3 edit.py brut.mp4 --broll broll/ --out jour002.mp4

Ce qu'il fait, dans l'ordre :
  1. Transcrit la parole avec les timecodes de chaque mot (Whisper, local, gratuit)
  2. Coupe les silences et les hésitations ("um", "uh", "like"...)
  3. Place ton B-roll aux moments où tu prononces le mot-clé du nom de fichier
  4. Grave des sous-titres style TikTok (2-3 mots a la fois)
  5. Exporte en 1080x1920

Le B-roll se place par NOM DE FICHIER. Nomme tes clips avec le mot que tu dis
dans la video : emails.mp4 se place quand tu dis "emails", quote.png quand tu
dis "quote". Plusieurs mots : separe-les par des tirets (supplier-factory.mp4).
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# ----------------------------------------------------------------------------
# Reglages
# ----------------------------------------------------------------------------

SILENCE_MAX = 0.55      # secondes de silence tolerees avant de couper
PAD = 0.06              # marge gardee autour de chaque segment de parole
BROLL_MIN = 1.2         # duree minimum d'un plan de B-roll
BROLL_MAX = 3.0         # duree maximum d'un plan de B-roll
BROLL_GAP = 2.5         # secondes minimum entre deux B-rolls
CAPTION_WORDS = 3       # mots par carton de sous-titre
W, H = 1080, 1920       # format de sortie

FILLERS = {
    "um", "uh", "euh", "hmm", "mmm", "erm", "ah", "eh",
    "like", "so", "yeah", "okay", "ok", "right",
}

VIDEO_EXT = {".mp4", ".mov", ".m4v", ".webm", ".mkv"}
IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".heic"}


# ----------------------------------------------------------------------------
# Utilitaires
# ----------------------------------------------------------------------------

def run(cmd, **kw):
    """Lance une commande et arrete tout si elle echoue."""
    proc = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if proc.returncode != 0:
        sys.stderr.write("\nEchec : %s\n" % " ".join(str(c) for c in cmd[:6]))
        sys.stderr.write(proc.stderr[-2500:] + "\n")
        sys.exit(1)
    return proc


def need(binary, hint):
    if shutil.which(binary) is None:
        sys.exit("Il manque '%s'. %s" % (binary, hint))


def duration_of(path):
    proc = run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                "-of", "default=nw=1:nk=1", str(path)])
    return float(proc.stdout.strip())


def esc(path):
    """Echappe un chemin pour l'interieur d'un filtre ffmpeg."""
    return str(path).replace("\\", "/").replace(":", "\\:").replace("'", "\\'")


# ----------------------------------------------------------------------------
# 1. Transcription
# ----------------------------------------------------------------------------

def transcribe(video, language, model_size):
    """Retourne [{word, start, end}, ...] avec les timecodes de chaque mot."""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit(
            "Il manque faster-whisper.\n"
            "  pip install faster-whisper\n"
        )

    print("  Transcription (%s, modele %s)..." % (language or "auto", model_size))
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, _ = model.transcribe(
        str(video), language=language, word_timestamps=True, vad_filter=True
    )

    words = []
    for seg in segments:
        for w in (seg.words or []):
            text = w.word.strip()
            if text:
                words.append({"word": text, "start": float(w.start), "end": float(w.end)})
    if not words:
        sys.exit("Aucune parole detectee. Verifie le son de ta video.")
    print("  %d mots detectes." % len(words))
    return words


# ----------------------------------------------------------------------------
# 2. Plan de coupe
# ----------------------------------------------------------------------------

def normalize(word):
    return re.sub(r"[^\w']", "", word.lower())


def build_cuts(words, total):
    """Garde la parole, jette les silences longs et les hesitations."""
    kept = [w for w in words if normalize(w["word"]) not in FILLERS]
    dropped = len(words) - len(kept)

    segments = []
    for w in kept:
        start = max(0.0, w["start"] - PAD)
        end = min(total, w["end"] + PAD)
        if segments and start - segments[-1][1] <= SILENCE_MAX:
            segments[-1][1] = max(segments[-1][1], end)
        else:
            segments.append([start, end])

    print("  %d hesitations coupees, %d segments gardes." % (dropped, len(segments)))
    return segments, kept


def remap(words, segments):
    """Recalcule les timecodes des mots sur la nouvelle ligne de temps."""
    out = []
    elapsed = 0.0
    for seg_start, seg_end in segments:
        seg_len = seg_end - seg_start
        for w in words:
            mid = (w["start"] + w["end"]) / 2.0
            if seg_start <= mid < seg_end:
                out.append({
                    "word": w["word"],
                    "start": elapsed + max(0.0, w["start"] - seg_start),
                    "end": elapsed + min(seg_len, w["end"] - seg_start),
                })
        elapsed += seg_len
    out.sort(key=lambda w: w["start"])
    return out, elapsed


# ----------------------------------------------------------------------------
# 3. Placement du B-roll
# ----------------------------------------------------------------------------

def load_broll(folder):
    """Chaque fichier devient un mot-cle tire de son nom."""
    if not folder:
        return []
    folder = Path(folder)
    if not folder.is_dir():
        sys.exit("Dossier de B-roll introuvable : %s" % folder)

    clips = []
    for path in sorted(folder.iterdir()):
        ext = path.suffix.lower()
        if ext not in VIDEO_EXT and ext not in IMAGE_EXT:
            continue
        keywords = [normalize(k) for k in re.split(r"[-_\s]+", path.stem) if normalize(k)]
        if not keywords:
            continue
        clips.append({
            "path": path,
            "keywords": keywords,
            "is_image": ext in IMAGE_EXT,
            "used": False,
        })
    print("  %d clips de B-roll charges." % len(clips))
    return clips


def plan_broll(words, clips, timeline):
    """Trouve ou chaque clip doit apparaitre, selon les mots prononces."""
    plan = []
    heard = set()
    for w in words:
        token = normalize(w["word"])
        if not token:
            continue
        for clip in clips:
            if clip["used"] or token not in clip["keywords"]:
                continue
            heard.add(clip["path"].name)
            start = w["start"]
            if plan and start - plan[-1]["end"] < BROLL_GAP:
                continue

            if clip["is_image"]:
                length = BROLL_MIN
            else:
                length = max(BROLL_MIN, min(BROLL_MAX, duration_of(clip["path"])))

            end = min(timeline, start + length)
            if end - start < 0.5:
                continue

            clip["used"] = True
            plan.append({"path": clip["path"], "is_image": clip["is_image"],
                         "start": start, "end": end, "word": token})
            break

    for item in plan:
        print("     %5.1fs  %-22s  (\"%s\")" % (item["start"], item["path"].name, item["word"]))

    jamais_dit = [c["path"].name for c in clips
                  if not c["used"] and c["path"].name not in heard]
    trop_serre = [c["path"].name for c in clips
                  if not c["used"] and c["path"].name in heard]
    if jamais_dit:
        print("  Ignores, le mot-cle n'est jamais dit : %s" % ", ".join(jamais_dit))
    if trop_serre:
        print("  Ignores, trop proches du B-roll precedent (BROLL_GAP = %.1f s) : %s"
              % (BROLL_GAP, ", ".join(trop_serre)))
    return plan


# ----------------------------------------------------------------------------
# 4. Sous-titres
# ----------------------------------------------------------------------------

ASS_HEADER = """[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Main,Arial Black,{size},&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,7,3,2,90,90,{margin},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def ass_time(seconds):
    seconds = max(0.0, seconds)
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    return "%d:%02d:%05.2f" % (h, m, s)


def write_captions(words, path):
    """Sous-titres style court metrage : 3 mots a la fois, gros, centres bas."""
    lines = [ASS_HEADER.format(w=W, h=H, size=int(H * 0.042), margin=int(H * 0.20))]
    for i in range(0, len(words), CAPTION_WORDS):
        group = words[i:i + CAPTION_WORDS]
        text = " ".join(g["word"] for g in group).upper().replace("\n", " ")
        text = text.replace("{", "").replace("}", "")
        lines.append("Dialogue: 0,%s,%s,Main,,0,0,0,,%s" % (
            ass_time(group[0]["start"]), ass_time(group[-1]["end"]), text))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("  %d cartons de sous-titres." % ((len(words) + CAPTION_WORDS - 1) // CAPTION_WORDS))


# ----------------------------------------------------------------------------
# 5. Rendu
# ----------------------------------------------------------------------------

def cut_pass(source, segments, out_path):
    """Applique le plan de coupe en une passe."""
    expr = "+".join("between(t,%.3f,%.3f)" % (s, e) for s, e in segments)
    run([
        "ffmpeg", "-y", "-i", str(source),
        "-vf", "select='%s',setpts=N/FRAME_RATE/TB" % expr,
        "-af", "aselect='%s',asetpts=N/SR/TB" % expr,
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        str(out_path),
    ])


def render(cut_video, broll_plan, captions, out_path):
    """Recadre en vertical, superpose le B-roll, grave les sous-titres."""
    cmd = ["ffmpeg", "-y", "-i", str(cut_video)]

    for item in broll_plan:
        if item["is_image"]:
            cmd += ["-loop", "1", "-t", "%.3f" % (item["end"] - item["start"]),
                    "-i", str(item["path"])]
        else:
            cmd += ["-i", str(item["path"])]

    fit = ("scale={w}:{h}:force_original_aspect_ratio=increase,"
           "crop={w}:{h},setsar=1").format(w=W, h=H)

    steps = ["[0:v]%s[base]" % fit]
    current = "base"
    for idx, item in enumerate(broll_plan, start=1):
        label = "b%d" % idx
        # Decale le clip pour qu'il tombe dans sa fenetre d'affichage :
        # sans ca, il joue a t=0 et il est deja fini quand l'overlay s'active.
        steps.append("[%d:v]%s,fps=30,setpts=PTS-STARTPTS+%.3f/TB[%s]"
                     % (idx, fit, item["start"], label))
        nxt = "v%d" % idx
        steps.append(
            "[%s][%s]overlay=0:0:enable='between(t,%.3f,%.3f)':eof_action=pass[%s]"
            % (current, label, item["start"], item["end"], nxt)
        )
        current = nxt

    steps.append("[%s]subtitles='%s'[out]" % (current, esc(captions)))

    cmd += [
        "-filter_complex", ";".join(steps),
        "-map", "[out]", "-map", "0:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "20",
        "-pix_fmt", "yuv420p", "-r", "30",
        "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        str(out_path),
    ]
    run(cmd)


# ----------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Monte automatiquement une video parlee verticale.")
    ap.add_argument("video", help="ta video brute")
    ap.add_argument("--broll", help="dossier contenant tes clips et captures d'ecran")
    ap.add_argument("--out", default="monte.mp4", help="fichier de sortie")
    ap.add_argument("--lang", default="en", help="langue parlee (en, fr...)")
    ap.add_argument("--model", default="base",
                    help="taille du modele Whisper : tiny, base, small, medium")
    ap.add_argument("--keep-fillers", action="store_true",
                    help="garde les hesitations au lieu de les couper")
    args = ap.parse_args()

    need("ffmpeg", "Installe-le : https://ffmpeg.org/download.html")
    need("ffprobe", "Il vient avec ffmpeg.")

    source = Path(args.video)
    if not source.is_file():
        sys.exit("Video introuvable : %s" % source)

    if args.keep_fillers:
        FILLERS.clear()

    total = duration_of(source)
    print("\nVideo brute : %s  (%.1f s)" % (source.name, total))

    print("\n[1/5] Transcription")
    words = transcribe(source, args.lang, args.model)

    print("\n[2/5] Plan de coupe")
    segments, kept = build_cuts(words, total)

    work = Path(tempfile.mkdtemp(prefix="montage-"))
    try:
        print("\n[3/5] Coupe")
        cut_video = work / "cut.mp4"
        cut_pass(source, segments, cut_video)
        timed, timeline = remap(kept, segments)
        print("  %.1f s -> %.1f s  (%.0f %% enleve)"
              % (total, timeline, 100 * (1 - timeline / total) if total else 0))

        print("\n[4/5] B-roll")
        clips = load_broll(args.broll)
        plan = plan_broll(timed, clips, timeline) if clips else []

        print("\n[5/5] Sous-titres et rendu")
        captions = work / "captions.ass"
        write_captions(timed, captions)
        render(cut_video, plan, captions, Path(args.out))

        summary = Path(args.out).with_suffix(".json")
        summary.write_text(json.dumps({
            "source": str(source),
            "duree_brute": round(total, 2),
            "duree_montee": round(timeline, 2),
            "segments": len(segments),
            "broll": [{"fichier": p["path"].name, "a": round(p["start"], 2),
                       "mot": p["word"]} for p in plan],
            "transcript": " ".join(w["word"] for w in timed),
        }, ensure_ascii=False, indent=2), encoding="utf-8")

        print("\nFini : %s" % args.out)
        print("Detail : %s" % summary)
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    main()
