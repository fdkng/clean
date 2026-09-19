# Contexte pour le montage

Ce dossier sert à monter une vidéo par jour. Lis ce fichier avant de monter.

**Ce sont mes préférences par défaut, pas des règles fixes.** Si je te demande
autre chose dans la conversation, ma demande passe avant ce fichier. Tu
n'exécutes aucun script préfabriqué : tu écris le ffmpeg qu'il faut, à chaque
fois, selon ce que je te dis.

---

## La série

Je documente un programme d'affaires de 336 jours que je me suis écrit
moi-même. Trois vidéos de cours par jour, puis je publie une vidéo d'environ
une minute sur ce que j'ai appris. Je parle en anglais, face caméra.

Le sujet, c'est **l'apprentissage**, et c'est aussi le produit. Le programme
lui-même est ce que je vends : je le construis en public, un jour à la fois, et
les gens qui me suivent peuvent l'acheter au complet. Il n'y a plus de business
cachée en arrière-plan à ménager — ce que je montre est ce que je vends.

## La structure d'une vidéo

| Créneau | Temps | Contenu |
|---|---|---|
| 1 | 0-6 s | Le résultat de ce que je m'étais engagé à faire la veille |
| 2 | 6-13 s | Le numéro du jour, le thème, les trois intervenants |
| 3 | 13-36 s | Ma réponse de pré-test, puis ce sur quoi les trois convergent |
| 4 | 36-44 s | Ce que j'aurais fait si je l'avais su avant |
| 5 | 44-53 s | Ce que je fais ce soir à cause de ça |
| 6 | 53-59 s | Un ordre d'agir, puis le jour suivant |

Le créneau 3 est le cœur. S'il faut couper pour raccourcir, coupe le 4 avant
tout le reste, et jamais le 3.

## Je donne l'ordre, tu trouves les prises

Chaque jour je t'envoie un **plan** : une ligne par idée, dans l'ordre où elles
doivent passer, avec quelques mots de ce que je dis à ce moment-là.

```
1. l'engagement d'hier — 15 fournisseurs, 5 ont repondu
2. le jour, le theme, les trois intervenants
3. voix off — les trois tests
4. j'ai echoue le troisieme
5. [Remotion] ce que je fais ce soir
6. [Remotion] l'ordre d'agir + le jour suivant
```

Deviner la structure n'est pas ton travail. Le tien, c'est :

1. retrouver dans les rushes le passage qui correspond à chaque ligne du plan
2. en garder la meilleure prise
3. monter dans l'ordre que j'ai donné, sans le réorganiser

Une ligne du plan sans clip correspondant : dis-le-moi, ne comble pas. Un clip
qui ne correspond à aucune ligne : dis-le aussi — c'est soit une prise que j'ai
oubliée de mettre au plan, soit du matériel à jeter.

Les lignes marquées `[Remotion]` n'existent pas en vidéo : c'est à construire en
typographie animée.

## Mes rushes sont des prises, pas un montage

Chaque jour je filme la même ligne plusieurs fois. Je me trompe, je bégaie, je
recommence. **Rien de ce que je te donne n'est une version finale.** Un dossier
de rushes, c'est de la matière brute avec des ratés dedans.

Ta job, pour chaque phrase du script : retrouver **toutes** les prises de cette
phrase et **garder la meilleure**.

Comment trancher :

- Écarte toute prise où je me reprends en plein milieu
- Écarte celles où je bute sur un mot ou je perds le fil
- À qualité égale, prends la **dernière** : c'est presque toujours la plus assurée
- Si deux prises sont bonnes mais différentes, montre-les-moi et laisse-moi choisir

Ne colle jamais deux prises de la même phrase bout à bout, et ne prends pas la
première venue parce qu'elle arrive en premier dans le fichier.

Dis-moi toujours, pour chaque ligne : combien de prises tu as trouvées, laquelle
tu as retenue, et pourquoi.

## Va chercher ce dont je parle

Quand je nomme une vidéo, une personne ou un livre, **montre la vraie chose** :
la vignette de la vidéo YouTube en question, la couverture du livre, la page
citée. C'est ce dont je parle, à l'écran, pendant que j'en parle.

Les vignettes se récupèrent avec `yt-dlp` :

```
yt-dlp --write-thumbnail --skip-download --convert-thumbnails png "<url>"
```

Si je ne t'ai pas donné les liens, demande-les-moi — je les ai dans mon
programme. N'invente pas une image approchante.

**Ce n'est pas de la banque d'images.** La distinction est simple :

- **La chose exacte dont je parle** — la vignette de la vidéo que j'ai écoutée,
  ma soumission, mon courriel, mon document à l'écran : c'est une preuve, ça va
- **Une image générique qui illustre l'idée** — une poignée de main pour
  « fournisseur », une pile de billets pour « argent » : jamais

Une prise où je bégaie est écartée complètement, son et image. Ne la réutilise
pas comme fond.

## Quand je te dis que c'est deja coupe

Certains jours je te donne un fichier que j'ai **deja monte moi-meme**. Je te le
dis explicitement.

Dans ce cas : **tu ne coupes rien.** Pas un silence, pas une hesitation, pas une
respiration. Le rythme est deja decide, ce n'est plus ton travail.

Tu fais le reste : sous-titres, animations, etalonnage, son, export. Si tu penses
qu'une coupe ameliorerait quelque chose, **dis-le-moi et attends** — ne la fais
pas.

## Ne coupe jamais dans une phrase

Un silence a la fin d'une phrase est de la **ponctuation**, pas du vide mort.

Entre « When was the last time it happened? » et « What did you try? », le
silence fait partie de la livraison. Le supprimer colle les deux phrases et ca
s'entend immediatement.

Avant toute coupe :

- Verifie que la phrase est **terminee** — dernier mot prononce en entier, pas
  coupe sur sa syllabe finale
- Laisse au moins **250 ms** apres le dernier mot avant de couper
- Ne coupe jamais entre deux phrases d'une meme idee enumeree

La regle du demi-seconde vise les vrais blancs : quand je cherche mes mots,
quand je relis mes notes, quand je repars une prise. Pas les respirations d'une
phrase a l'autre.

## Comment monter

**Les coupes.** Enlève les silences de plus d'une demi-seconde et mes
hésitations : *um*, *uh*, *like*, *so* en début de phrase. Garde une petite
marge autour de chaque mot pour que ça respire — une coupe collée sur la
syllabe s'entend.

**Les sous-titres.** Gravés dans l'image, jamais en fichier séparé. Blancs,
contour noir épais, majuscules, environ trois mots à la fois, centrés dans le
bas sans toucher la zone d'interface des applications. Ils doivent rester
lisibles sur fond clair comme sur fond foncé.

**Le B-roll.** Plein écran, entre une et trois secondes, au moins deux
secondes et demie entre deux plans — sinon ça clignote.

**La sortie.** 1080x1920, H.264, audio AAC.

## Le nom des fichiers de B-roll

Le nom du fichier est le mot que je prononce dans la vidéo. `emails.png` se
place quand je dis « emails ». Plusieurs mots possibles : sépare-les par des
tirets, `supplier-factory.mp4`.

Place chaque clip à la première occurrence du mot. Si un mot n'est jamais
prononcé, dis-le-moi au lieu de placer le clip ailleurs.

**N'utilise jamais de banque d'images.** Mon B-roll, c'est mes preuves : mes
courriels, mes soumissions, mes listes écrites à la main, mes documents à
l'écran. Du stock générique détruit exactement ce qui me rend crédible.

## Le vocabulaire

**Cette règle a changé.** Avant, j'évitais de nommer mon produit pour ne pas
brouiller le classement du compte. Ce n'est plus le cas : le programme est le
produit, et le compte doit être classé là-dessus.

Dis « my program », « the 336 days », « day 47 of 336 ». Le nombre 336 revient
souvent, c'est voulu — c'est ce qui rend le projet reconnaissable.

Ce que je ne dis jamais : « diplôme », « certification », « garanti ». Je ne
promets aucun résultat, c'est juste pour apprendre. Si tu génères ou corriges du
texte à l'écran, ne me fais jamais promettre quelque chose.

## À ne jamais faire

- Ajouter une intro ou un logo animé au début
- Laisser un silence avant mon premier mot : la première syllabe est dans le
  premier quart de seconde
- Mettre de la musique par-dessus ma voix sans que je l'aie demandé
- Réencoder plusieurs fois inutilement, ça ramollit l'image

## Comment je veux que tu travailles

Dis-moi ce que tu fais au fur et à mesure. Quand tu as un doute sur un choix
qui change le rendu, demande-moi avant de rendre plutôt que de deviner.

Après chaque rendu, dis-moi la durée finale, combien de secondes tu as
enlevées, et où chaque B-roll a atterri.
