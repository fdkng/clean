# Banc d'essai — pousser l'outillage à fond

**Cette vidéo ne sera pas publiée.** Le but n'est pas qu'elle soit belle ou
cohérente : c'est de voir ce que chaque outil sait faire, et à quoi ça
ressemble pour vrai.

Source : ma vidéo du jour 3 dans `rushes/`, déjà coupée.

Vise le niveau **production**, pas le niveau application mobile. Si un effet
ressemble à un préréglage de CapCut, c'est raté — refais-le en plus ambitieux.

---

## Comment procéder

**Rends chaque test séparément**, en clip de 3 à 5 secondes, numéroté :
`test_01_zoom.mp4`, `test_02_souris.mp4`, etc.

Je les regarde un par un et je te dis lesquels valent la peine. **Ensuite
seulement** on assemble les gagnants sur la vidéo complète.

Après chaque test, dis-moi : ce que tu as utilisé, le temps de rendu, et ce que
tu n'as pas réussi à obtenir.

---

## Les sons — fabrique-les

Pas de banque de sons. Synthétise-les avec `sox`, c'est un des outils à tester :

- un **whoosh** pour les mouvements de caméra
- un **pop** sec pour l'apparition d'un élément
- un **impact** grave pour les moments forts

Garde-les discrets : -20 dB sous ma voix. Un son qu'on remarque est trop fort.

---

## Test 01 — Zoom punch sonorisé

À chaque coupe, un resserrement de 4 à 8 % en 200 ms, accélération sèche,
synchronisé avec un whoosh.

Fais **depuis l'original 4K**, pas depuis le proxy.

*Ce qu'on teste : recadrage dynamique + synchro son.*

## Test 02 — La souris qui clique (le gros morceau)

Quand je nomme Y Combinator, construis en Remotion une **maquette de page
YouTube** : le cadre du navigateur, la chaîne, la vignette de la vraie vidéo
(récupérée avec `yt-dlp --write-thumbnail`).

Un **curseur entre dans le cadre**, se déplace vers la vignette, clique — ondes
de clic, léger enfoncement — puis la caméra **plonge dans la vignette** qui
remplit l'écran.

Le tout en **perspective 3D** : la page légèrement inclinée, le curseur qui se
déplace dans l'espace, pas à plat.

*Ce qu'on teste : 3D CSS dans Remotion, animation de curseur, images réelles,
mouvement de caméra.*

## Test 03 — Typographie cinétique en 3D

Une phrase que je dis, en Anton, qui arrive **depuis la profondeur** : chaque
mot pivote sur son axe et se met en place, avec un décalage de 60 ms entre eux.
Perspective marquée, pas un simple agrandissement.

*Ce qu'on teste : `transform-style: preserve-3d`, `perspective`, décalage.*

## Test 04 — Le compteur à palettes

`001` bascule en `002` comme un afficheur de gare : la palette du haut tombe,
la nouvelle arrive, léger rebond. `spring({damping: 12, stiffness: 200})`.

Soigne l'ombre portée sur la palette qui tombe — c'est ce qui donne l'épaisseur.

*Ce qu'on teste : rotation 3D sur un axe, ombres, ressorts.*

## Test 05 — Révélation par masque

Une phrase qui apparaît **par un masque qui balaie**, pas par un fondu. Le texte
existe déjà, c'est le masque qui se déplace.

Essaie aussi la version inverse : le texte se fait effacer.

*Ce qu'on teste : masques et découpes en Remotion.*

## Test 06 — Glitch

Sur un mot dur, une décomposition **RVB** : les trois canaux se séparent de
quelques pixels, tremblent 150 ms, se recollent. Avec des lignes de balayage si
ça sert.

*Ce qu'on teste : `colorchannelmixer` et décalages en ffmpeg, ou filtres CSS
dans Remotion — compare les deux.*

## Test 07 — Passe cinéma

Sur 4 secondes : grain de film léger, aberration chromatique dans les coins,
vignettage discret, courbe de couleur plus froide dans les ombres.

Rends la **même seconde avec et sans**, côte à côte, pour que je voie la
différence.

*Ce qu'on teste : étalonnage, `zscale`, grain, LUT.*

## Test 08 — Empilement 3D

Mes trois tests (`URGENT?`, `UNIQUELY QUALIFIED?`, `NOTICED, NOT INVENTED?`)
qui s'empilent **en perspective**, comme des cartes posées l'une sur l'autre en
profondeur. Puis la caméra tourne légèrement autour de la pile.

Le troisième vire au rouge et se fait barrer pendant que la caméra bouge.

*Ce qu'on teste : profondeur, caméra virtuelle, animation pendant un
déplacement.*

---

## Ce que je veux à la fin

Les huit clips, plus un mot sur chacun : **ce qui a bien rendu, ce qui a l'air
cheap, ce que l'outil ne sait pas faire.**

Sois franc. Un effet raté qu'on identifie vaut mieux qu'un effet moyen qu'on
garde.
