# Dossier de montage

Un dossier, une vidéo par jour, aucun script figé.

## Ce qu'il faut sur la machine

- **ffmpeg** — `brew install ffmpeg`
- **L'app Claude** — session locale ouverte sur ce dossier

## Comment s'en servir

Mets ta vidéo brute et tes captures d'écran dans le dossier :

```
jour002/
├── brut.mp4
└── broll/
    ├── emails.png
    └── quote.png
```

Ouvre une session Claude **locale** sur ce dossier et demande ce que tu veux,
en français. `CLAUDE.md` contient déjà tes préférences — pas besoin de les
répéter.

> Monte `brut.mp4`. Les captures sont dans `broll/`. Sors-moi `jour002.mp4`.

Puis tu corriges en parlant :

> Les sous-titres sont trop bas.
> Mets une police plus condensée.
> Les mots apparaissent un par un au lieu de trois d'un coup.
> Le B-roll rentre en fondu au lieu de couper sec.
> Fais grossir le mot quand je le prononce.

Rien n'est figé. Une demande différente donne un montage différent.

## Vérifier qu'une session est locale

Demande `uname -a`. Si ça répond **Darwin**, tu es sur ton Mac. Si ça répond
**Linux**, la session roule dans le nuage et n'a pas accès à tes fichiers.

## Garde tes fichiers bruts

Un dossier par jour, daté, avec la vidéo non montée dedans. C'est la seule
pièce qui ne se rattrape pas plus tard.

---

# Studio — l'interface

Une page web locale pour monter en parlant, au lieu de taper dans un terminal.

```
cd ~/Desktop/montage
python3 studio.py
```

Le navigateur s'ouvre sur `http://localhost:8765`.

## Comment ça marche

- **Glisse tes vidéos et tes captures dans la page** — elles atterrissent dans
  le dossier
- **Écris ce que tu veux dans la barre du bas** (Cmd+Entrée pour envoyer)
- L'agent monte, sa sortie défile en direct, le résultat s'affiche dans le
  lecteur
- Tu continues à lui parler pour corriger

## Ce que ça fait tourner

La page ne monte rien elle-même. Elle passe ta demande au **Claude Code déjà
installé sur ta machine**, dans ce dossier, qui lit `CLAUDE.md`, écrit le
ffmpeg qu'il faut et le lance.

Rien ne sort de ton Mac : le serveur écoute sur `127.0.0.1` seulement, et les
fichiers ne quittent jamais le dossier.

## Ce que tu autorises

Pour lancer ffmpeg sans t'interrompre à chaque commande, le studio pré-approuve
`Bash,Read,Write,Edit,Glob,Grep` pour l'agent — dans ce dossier uniquement.
C'est la constante `CLAUDE_FLAGS` en haut de `studio.py` si tu veux resserrer.

Lance le studio depuis ton dossier de montage, pas depuis ton dossier
personnel.

## Exemples de demandes

> Monte brut.mp4, mes captures sont dans broll/, sors-moi jour002.mp4

> Analyse ref.mp4 : extrais des images, regarde le style des sous-titres, la
> fréquence des coupes, les zooms. Montre-moi ton analyse, puis applique ce
> style à brut.mp4.

> Les sous-titres sont trop bas, monte-les de 10 %.

> Fais grossir le mot quand je le prononce.

> Retiens ça dans CLAUDE.md.

## Changer d'agent

Le studio pilote Claude Code par défaut. Pour Codex :

```
STUDIO_AGENT=codex python3 studio.py
```

Le nom de l'agent s'affiche au démarrage. `AGENTS.md` pointe sur `CLAUDE.md`,
donc les deux lisent le même contexte — rien à dupliquer.

Installer Codex et lui donner les mêmes outils :

```
npm install -g @openai/codex
npx ffmpeg-skill --codex
```

Les skills Remotion sont déjà en place pour Codex : elles ont été installées
dans `.agents/skills`, que les deux agents lisent.

Si le lancement échoue sur un drapeau inconnu, la commande exacte s'affiche
dans l'erreur — les profils sont en haut de `studio.py`, dans `AGENTS`.
