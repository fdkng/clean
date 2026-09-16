# Brief de montage — Jour 002

Tout est décidé. Suis ce document, ne redemande pas les choix déjà tranchés.
Une version existe (`final_day2_v2.mp4`) : regarde-la pour situer la cible,
mais refais le montage depuis les rushes.

Sortie : `jour002_final.mp4`, 1080×1920, H.264, AAC, ~48 s.

---

## 1. Les prises — déjà choisies

Ne cherche pas d'autres passages, ne recoupe pas ailleurs.

| Segment | Fichier | Timecodes |
|---|---|---|
| Engagement d'hier | `A001_0914403 p.m._C002.MOV` | 3.26 → 6.54 |
| Les trois noms | `A001_0914406 p.m._C006.MOV` | 1.32 → 5.54 |
| Le thème | `A001_0914403 p.m._C004.MOV` | 30.14 → 33.46 |
| Voix off — intro | `IMG_7998.MOV` | 16.02 → 21.48 |
| Voix off — transition | `IMG_7998.MOV` | 24.20 → 27.62 |
| Voix off — test 1 | `IMG_7998.MOV` | 39.72 → 42.96 |
| Voix off — test 3 | `IMG_7998.MOV` | 160.08 → 165.96 |
| La confession | `A001_0914346 p.m._C002.MOV` | 28.44 → 32.94 |
| Le CTA | `A001_0914355 p.m._C008.MOV` | 0.00 → 1.12 puis 2.12 → 6.06 |

**Le test 2 n'existe pas en audio.** Toutes les prises sont bafouillées. Il
passe en carton seulement, tenu ~1,5 s entre le test 1 et le test 3, sans voix.

Les noms se prononcent **Jared Friedman**, **Michael Seibel**, **Paul Graham** —
la transcription automatique les écorche, corrige-les partout.

---

## 2. Identité visuelle — non négociable

**Police : Anton.** Partout, cartons comme sous-titres gravés. Jamais deux
polices dans la même vidéo.

| Couleur | Ce que ça signifie |
|---|---|
| Doré `#D9AE5C` | le cadre — le compteur de jours, les tests |
| Blanc | mes mots à moi |
| Rouge `#D2635A` | l'échec |

**Sous-titres** : gravés, majuscules, contour noir épais, 3 mots maximum à
l'écran, révélation mot par mot calée sur mon débit réel — pas sur un tempo
imposé.

---

## 3. Motion design

**Principe : rien n'apparaît sur place. Tout arrive de quelque part et repart
quelque part.**

### Le compteur — la signature

`DAY 2` n'est pas un carton fixe. `001` bascule en `002` comme un afficheur à
palettes : la palette du haut tombe, le nouveau chiffre arrive, léger rebond.
`spring({damping: 12, stiffness: 200})`, 600 ms.

À la fin, `002` bascule en `003` avec `TOMORROW` dessous. Même mécanisme aux
deux bouts — c'est ce qui ouvre et ferme chaque vidéo de la série.

### Les chiffres (0 → 3,5 s) — arithmétique visuelle

Sur « fifteen », **15 traits verticaux dorés** apparaissent en cascade, 40 ms
d'écart. Sur « five », **10 d'entre eux s'éteignent en gris** un par un,
rapidement. Il en reste 5, dorés.

Aucun chiffre écrit : on voit le ratio au lieu de le lire.

### Les trois tests — une liste qui se construit, puis se brise

Chaque test **glisse depuis la gauche**, son numéro en doré devant, avec un
**filet doré fin qui se trace dessous** de gauche à droite en 300 ms. Il reste à
l'écran, le suivant se pose en dessous.

- Test 1 validé : un **crochet doré** se trace à droite
- Test 2 : pareil
- Test 3 : le crochet commence à se tracer — puis **il pivote et devient un X
  rouge**, pendant que la barre traverse le texte de gauche à droite en 250 ms
  et que tout le bloc vire au rouge

**Ce pivot dure 400 ms, pas 150.** C'est le moment le plus important de la
vidéo : l'image dit que j'ai échoué une seconde avant que ma voix le dise.

### Pendant la confession

Les trois tests **rétrécissent et migrent en haut à gauche**, le 3 toujours
rouge barré. La preuve reste à l'écran pendant que j'avoue.

Sur le plan lui-même :

- **Resserrement de 8 à 9 % sur 600 ms**, accélération douce. Fais-le depuis
  l'**original 4K** dans `rushes/`, jamais depuis le proxy : recadrer ~972×1728
  dans du 3840×2160 puis remonter en 1080×1920 ne perd rien.
- **Désaturation à 35 % sur 400 ms**, synchronisée avec le virage du carton.
  Le rouge `#D2635A` du carton reste pleinement saturé — l'image se vide de sa
  couleur et le seul rouge qui reste, c'est l'échec. Retour à 100 % sur 300 ms
  à la fin du plan.

### Le fond — jamais noir

Mon image en dessous **partout** où il y a un carton ou de la voix off :
luminosité 35 %, saturation 40 %. Prends n'importe quel passage silencieux de
`346_C002` ou `IMG_7998` et boucle-le au besoin.

La synchronisation labiale n'est pas un problème à cette luminosité, avec la
typo qui domine : l'œil lit une couche de design. Un fond noir, lui, se lit
comme une panne.

Par-dessus : un **filet doré vertical à 8 % d'opacité** le long du bord gauche,
descente très lente.

### Les transitions

Jamais de coupe entre deux cartons. Le sortant **glisse vers le haut**, l'entrant
**monte du bas**, 350 ms, `Easing.out(Easing.cubic)`.

### Les règles de mouvement

- Entrées : `spring({damping: 14, stiffness: 180, mass: 0.6})`
- Sorties : linéaires, 200 ms — on sort plus vite qu'on entre
- Rien sous 150 ms ni au-dessus de 600 ms, sauf le pivot (400) et le compteur (600)
- Tout mouvement part ou arrive **hors du cadre**, jamais un fondu sur place
- Aucune rotation décorative, aucun rebond mou

---

## 4. Le reste

- Carton `TONIGHT I RUN MY BUSINESS THROUGH ALL THREE` : **3 secondes maximum**,
  mot par mot. Jette `IN WRITING`.
- Coupe les silences de plus d'une demi-seconde et les hésitations, avec une
  petite marge autour de chaque mot.
- **Normalise à -14 LUFS.**

---

## 5. Avant de rendre

Rends-moi d'abord **deux clips de 2 secondes** :

1. le compteur qui bascule de `001` à `002`
2. le crochet du test 3 qui pivote en X rouge

Je valide ces deux mouvements avant que tu montes les 48 secondes.
