# Tout l'outillage vidéo

Tâche pour l'agent local. Le but : que rien ne bloque jamais un montage parce
qu'un outil manque.

**Vérifie l'existant avant d'installer.** Plusieurs choses sont déjà là.
N'écrase rien qui fonctionne, ne casse pas ffmpeg pour ajouter un filtre.
Signale-moi chaque installation avant de la lancer si elle remplace un binaire
existant.

---

## 1. ffmpeg complet — la priorité

C'est le socle. Il lui faut **tous** les filtres, pas un build partiel.

Doivent répondre : `drawtext` (texte gravé), `subtitles` et `ass` (sous-titres
stylés), `zscale`, `colorchannelmixer`, `loudnorm`, `xfade`, `scale`, `crop`,
`overlay`, `select`, `atempo`, `silencedetect`.

```
ffmpeg -filters | grep -E "drawtext|subtitles|^ .ass|zscale|loudnorm|xfade"
ffmpeg -version | tr ' ' '\n' | grep -E "freetype|harfbuzz|fribidi|libass|libx264|libx265|videotoolbox"
```

Ce qui manque, répare-le. Préfère une réinstallation propre à une compilation
maison si les deux donnent le même résultat.

**Preuve** : un clip de 2 s, 1080×1920, mot `TEST` en Anton doré `#D9AE5C`,
fait **uniquement avec `drawtext`** → `drawtext_test.mp4`.

## 2. Remotion et son navigateur

Remotion rend ses animations dans un Chrome sans interface. Sans navigateur, pas
de motion design.

Trouve si un Chrome ou Chromium existe déjà sur la machine et si Remotion peut
être pointé dessus. Sinon, fais-lui télécharger le sien — une seule fois.

**Preuve** : un rendu Remotion de 2 s qui sort un fichier.

## 3. Transcription locale

Pour les timecodes mot par mot des sous-titres, sans rien envoyer en ligne.

Vérifie ce qui est déjà installé (`whisper`, `whisper-cpp`, `faster-whisper`) et
complète. Je veux des **timecodes au mot**, pas à la phrase.

**Preuve** : transcris 10 s d'un de mes rushes et montre-moi les timecodes.

## 4. Analyse d'une vidéo de référence

Je donne souvent un TikTok en exemple et je demande d'en reprendre le rythme.
Il faut pouvoir le **mesurer**, pas l'estimer à l'œil :

- détection de plans et fréquence de coupe (PySceneDetect ou équivalent)
- pics audio et leur position
- inspection technique fine (`mediainfo`)

**Preuve** : mesure la fréquence de coupe de `ref.mp4` et donne-moi la moyenne.

## 5. Images et cartons

Pour fabriquer du texte et des cartons sans passer par Remotion quand c'est plus
simple : **ImageMagick**.

**Preuve** : génère un PNG 1080×1920 avec du texte Anton doré centré.

## 6. Audio

- normalisation en LUFS (déjà dans ffmpeg)
- réduction de bruit et traitement fin : **sox**
- mesure de niveau et de silences

**Preuve** : mesure le LUFS d'un de mes rushes.

## 7. Polices

**Anton** est installée. Ajoute deux ou trois alternatives condensées et grasses
pour que j'aie du choix quand je voudrai changer : Archivo Black, Bebas Neue,
Oswald.

**Preuve** : liste-les et confirme que ffmpeg les voit.

## 8. Téléchargement

`yt-dlp` est là. Vérifie qu'il est à jour.

---

## Ce que je veux en retour

Un tableau : **outil · déjà là ou installé · la preuve qui a marché · ce qui a
échoué**.

Pour ce qui échoue, dis-le au lieu de le contourner en silence. Et si une
installation demande d'assouplir le sandbox ou d'ouvrir le réseau, **demande-moi
avant**.
