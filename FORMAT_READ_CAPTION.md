# Format « Read Caption »

Format séparé de la série quotidienne. Ce n'est pas un jour du programme, c'est
une vidéo de recrutement. À sortir quand je veux faire entrer du monde neuf, pas
tous les jours.

---

## Pourquoi ce format marche

La vidéo **ne répond pas à la question qu'elle pose**. La réponse est dans la
description. Le spectateur arrête de scroller pour lire — et pendant qu'il lit,
**la vidéo continue de tourner en boucle**. La durée de visionnement monte
pendant qu'il lit un texte. C'est tout le truc.

Donc : la vidéo est courte, calme, et se coupe volontairement avant la réponse.
Si je réponds à l'écran, le format ne sert plus à rien.

**Le ton.** Posé. Pas de mains qui brassent, pas de débit accéléré, pas de
montée de voix à la fin des phrases. Un seul cadre fixe, je ne bouge pas. Le
désespoir, c'est le rythme, pas les mots — c'est là que ça se joue.

---

## 1. La vidéo (~33 s)

Anglais, face caméra, plan fixe, 1080x1920.

| Temps | Ce que je dis | Écran |
|---|---|---|
| 0:00-0:04 | *"Somebody asked me why I want to be financially free this young."* | Rien. Juste moi. |
| 0:04-0:09 | *"Like it's a weird thing to want at seventeen."* | — |
| 0:09-0:13 | *"I'm not going to answer that here."* | `READ CAPTION` apparaît |
| 0:13-0:16 | (silence, je soutiens la caméra) | `READ CAPTION` reste |
| 0:16-0:24 | *"Because most people can't answer it either. They want the money. They can't tell you what it's for."* | — |
| 0:24-0:29 | *"Mine's in the caption. Read it. Then answer yours."* | — |
| 0:29-0:33 | *"And if you want the thing I use on the days it doesn't work — comment 336."* | `COMMENT 336` |

**Le pivot est à 0:16.** C'est la ligne qui fait que je ne quête pas : je
retourne la question sur le spectateur. Sans elle, c'est juste un ado qui parle
de son argent. Avec elle, c'est lui qui se sent visé.

**Le silence de 0:13 à 0:16 ne se coupe pas.** Il fait partie de la livraison.
C'est le trou où il a le temps de décider d'aller lire.

### Le carton `READ CAPTION`

- Apparaît à 0:09, reste jusqu'à la fin
- Position : **tiers supérieur**, pas en bas — le bas est mangé par l'interface
  et par le début de la description
- Typo Anton, blanc, contour noir mince. Pas d'or : l'or c'est le vocabulaire de
  la série, ça ici c'est une instruction
- Entrée : fondu 200 ms + montée de 12 px. Pas de pop, pas de rebond
- Une flèche `↓` sous le texte, immobile

### Les sous-titres — **décision à prendre**

Les sous-titres par défaut (majuscules, contour noir épais, trois mots) sont
faits pour un débit rapide. Ici ils vont crier par-dessus une vidéo calme.

Ma proposition pour **ce format seulement** : mêmes sous-titres mais **phrase
complète par carton** au lieu de trois mots, et pas de majuscules. Ça descend le
rythme visuel au niveau du rythme de la voix.

**Je ne le fais pas avant que tu tranches.** Dis-moi : sous-titres normaux, ou
version calme.

---

## 2. La description

Les deux premières lignes sont tout ce qui s'affiche avant le « plus ». Elles
doivent payer le clic à elles seules.

```
Why do I want money?

Not for a car.

To be free. To be able to take care of my family — all of them.
To travel when I feel like it.

And mostly: to have the choice.

The choice to decide one morning that I'm getting on a plane, because I feel
like it. The choice to decide one morning that I'm taking my family to the
movies. The choice to decide one night that we're going to a restaurant — and
that I'm paying for all of them.

That's it. That's the whole thing.

I'm 17. I left school. I wrote myself a 336-day program out of everything I
wanted to learn, and I'm doing it in public, one day at a time. No degree at the
end. No promise that it works. Just the learning.

Comment 336 and I'll send you what I use on the days I don't feel like it.

Your turn. Why do you want it?
```

**Ce texte sort de mes mots, pas des siens.** Le cœur (« avoir le choix… de
décider un matin que je m'en vais en voyage… d'aller au restaurant et de tout
leur payer ») est traduit direct. Ne pas le polir davantage : c'est exactement
sa force qu'il soit ordinaire. Personne n'invente « payer le restaurant à sa
famille » comme raison de vouloir de l'argent. C'est ce qui prouve que c'est
vrai.

Le « No degree at the end. No promise that it works. » est ma position, mot pour
mot. Il reste.

---

## 3. Le mot-clé : `336`

**Recommandation : 336.**

- Personne d'autre ne l'utilise — zéro faux déclenchement
- Court, impossible à mal écrire
- Ça pose une question dans les commentaires : « c'est quoi 336 ? » — et chaque
  personne qui répond à ça fait du volume de commentaires gratuitement
- Ça plante le programme sans que j'aie à le vendre dans la vidéo

Alternative si je veux quelque chose qui parle tout seul : `CHOICE`. Plus clair,
mais ça ne crée aucune curiosité et ça risque d'attraper des commentaires qui
contiennent le mot sans demander le guide.

Dans ManyChat, configurer le déclencheur pour attraper `336`, `336 ` et `#336`.

---

## 4. Le DM automatique

### Message 1 — instantané

```
Hey — you commented 336.

Here's the guide. Five rules I use on the days I don't feel like it.
It's free, there's nothing to sign up for, and it takes about five
minutes to read.

<LIEN DU GUIDE>

Rule 1 is the one to do tonight, before you sleep. The rest can wait
until tomorrow.

— Louis-Félix
```

Le guide est une page web : **https://claude.ai/artifact/WxXAKVaGBFJZ2wPccS92YH**

Contenu : les cinq règles (décider la veille · un plancher que tu peux pas
manquer · publier le résultat pas le plan · jamais deux fois de suite · garder
le compte visible), chacune avec ce qui casse sans elle, le mécanisme, ma
version concrète, et l'action à faire le soir même. Plus une liste de quatre
cases à cocher à la fin.

**La page est privée tant que je ne la partage pas.** Avant de brancher
ManyChat : ouvrir la page, menu Partager, la rendre publique, et tester le lien
dans une fenêtre de navigation privée. Si le lien est mort, j'envoie un lien
mort à tout le monde qui a commenté.

### Message 2 — 24 h plus tard

```
Did you do the first one? Deciding the night before.

Genuinely asking — if you tell me which rule you picked I'll tell you
what broke for me on that one.
```

Une seule question, ouverte, qui appelle une réponse courte. C'est ce qui ouvre
la conversation. **Pas de pitch dans le message 2.** Rien à vendre avant qu'il
ait répondu au moins une fois.

---

## À vérifier avant de publier

- **ManyChat sur Instagram** : le compte doit être un compte pro, et le DM
  automatique à un commentateur ne part que si le déclencheur est bien un
  déclencheur « commentaire », pas un mot-clé de DM. Tester avec un deuxième
  compte avant de sortir la vidéo — si le DM ne part pas, j'ai promis quelque
  chose à tout le monde dans les commentaires pour rien.
- **La description doit être publiée en même temps que la vidéo**, évidemment,
  mais surtout : vérifier que les deux premières lignes ne sont pas tronquées
  par la plateforme. Sur TikTok c'est plus court que sur Instagram.
- Le mot `336` doit être visible à l'écran à la fin, pas juste dit. Du monde
  regarde sans son.

---

## Ce que ce format n'est pas

Ce n'est pas la vidéo quotidienne. La quotidienne enseigne quelque chose de
précis appris ce jour-là. Celle-ci n'enseigne rien — elle recrute. Ne pas mêler
les deux : si j'essaie de faire les deux dans la même vidéo, la question perd sa
tension et la leçon perd sa place.

Fréquence : quand j'en ai une vraie à poser. Pas sur un horaire.
