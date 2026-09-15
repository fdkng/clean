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
