# Monteur automatique — MBA de fondateur

Tu donnes une vidéo brute et un dossier de B-roll. Tu reçois une vidéo verticale
montée, coupée, sous-titrée.

```
python3 edit.py brut.mp4 --broll broll/ --out jour002.mp4
```

## Ce qu'il fait

1. **Transcrit** ta parole avec le timecode de chaque mot
2. **Coupe** les silences de plus d'une demi-seconde et les hésitations (*um*, *uh*, *like*…)
3. **Place ton B-roll** aux moments où tu prononces le mot-clé
4. **Grave les sous-titres** en gros, trois mots à la fois, centrés
5. **Exporte** en 1080×1920

Tout roule sur ta machine. Aucune clé d'API, aucun abonnement, rien qui monte
sur un serveur.

## Installation — une seule fois

**1. ffmpeg**

- macOS : `brew install ffmpeg`
- Windows : `winget install ffmpeg`
- Linux : `sudo apt install ffmpeg`

**2. Le reste**

```
pip install faster-whisper
```

Vérifie que ça marche :

```
ffmpeg -version
python3 edit.py --help
```

## Nommer ton B-roll

**Le nom du fichier, c'est le mot que tu dis dans la vidéo.**

| Fichier | Apparaît quand tu dis |
|---|---|
| `emails.mp4` | « emails » |
| `quote.png` | « quote » |
| `supplier-factory.mp4` | « supplier » ou « factory » |
| `mba.mp4` | « MBA » |

Un clip est utilisé **une seule fois**, à sa première occurrence. Si le mot-clé
n'est jamais prononcé, le clip est ignoré et le script te le dit.

Deux B-rolls gardent toujours 2,5 secondes d'écart, pour pas que ça clignote.

## Exemple

```
jour002/
├── brut.mp4
└── broll/
    ├── emails.png          ← capture de ton inbox
    ├── quote.png           ← la soumission de l'usine
    └── mba.mp4             ← ton document qui défile
```

```
python3 edit.py jour002/brut.mp4 --broll jour002/broll/ --out jour002.mp4
```

Sortie : `jour002.mp4` plus `jour002.json` — le détail de ce qui a été coupé,
où chaque B-roll a été placé, et le transcript complet.

## Options

| Option | Défaut | Quoi |
|---|---|---|
| `--lang` | `en` | Langue parlée : `en`, `fr`… |
| `--model` | `base` | Précision de la transcription : `tiny`, `base`, `small`, `medium` |
| `--keep-fillers` | — | Garde les hésitations |
| `--out` | `monte.mp4` | Nom du fichier de sortie |

`base` suffit pour une vidéo d'une minute. Monte à `small` si les sous-titres
se trompent souvent sur des mots précis (noms propres, chiffres).

## Réglages

Les constantes sont en haut de `edit.py` :

| Constante | Défaut | Quoi |
|---|---|---|
| `SILENCE_MAX` | `0.55` | Silence toléré avant de couper, en secondes |
| `BROLL_MIN` / `BROLL_MAX` | `1.2` / `3.0` | Durée d'un plan de B-roll |
| `BROLL_GAP` | `2.5` | Écart minimum entre deux B-rolls |
| `CAPTION_WORDS` | `3` | Mots par carton de sous-titre |

## Garde tes fichiers bruts

Un dossier par jour, daté, avec la vidéo brute non montée.

C'est la seule pièce qui se rattrape pas plus tard : le jour où tu voudras que
l'agent aille chercher du B-roll dans tes anciennes vidéos, il lui faudra une
archive. Elle se construit maintenant ou jamais.
