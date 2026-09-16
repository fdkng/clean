# Configurer Codex pour le montage

Tâche pour l'agent local. Le but : que Codex soit utilisable pour monter des
vidéos sans avoir à lui passer des drapeaux à chaque lancement.

Version installée au moment d'écrire : **OpenAI Codex v0.154.0**. Les noms
d'options changent d'une version à l'autre — **vérifie avant d'écrire**, ne te
fie pas aux noms cités ici.

---

## Commence par découvrir

Ne devine aucune clé de configuration. Lis d'abord :

```
codex --version
codex --help
codex exec --help
codex config --help        # si la sous-commande existe
```

Regarde aussi s'il existe déjà un fichier de configuration (`~/.codex/` ou
équivalent) et ce qu'il contient.

**Si une option que tu comptes utiliser n'apparaît nulle part, ne l'écris pas.**
Dis-le-moi à la place.

---

## L'état à atteindre

En lançant simplement `codex` dans `~/Desktop/montage`, sans aucun drapeau,
l'en-tête doit afficher :

| Champ | Valeur voulue | Pourquoi |
|---|---|---|
| `sandbox` | écriture dans le dossier de travail | sinon il ne peut ni monter ni écrire de fichier |
| `reasoning effort` | le maximum disponible | choisir des prises et écrire du Remotion demande de réfléchir |
| `approval` | pas de demande à chaque commande | sinon ffmpeg s'arrête à chaque appel |
| `model` | le plus capable auquel mon compte a droit | vérifie ce qui est disponible, ne suppose pas |

**L'accès réseau** : Remotion a besoin de `npm` pour installer ses dépendances.
Si le bac à sable le coupe, active-le — mais **dis-moi que tu l'actives** et
pourquoi, je veux savoir ce que j'autorise.

---

## Les outils qui doivent être visibles

Vérifie que Codex voit bien :

- **`ffmpeg-skill`** — installé dans `~/.agents/skills/ffmpeg-skill`
- **Les 12 skills Remotion** — installées dans `~/.agents/skills/`
- **`AGENTS.md`** du dossier — mes préférences de montage
- **`ffmpeg` 9.0.1** et **`Anton`** comme police système

Si l'une manque, installe-la et dis-moi laquelle.

---

## La preuve que ça marche

Ne me dis pas que c'est configuré : **montre-le**.

Depuis `~/Desktop/montage`, fais produire à Codex un clip de test de 2 secondes,
1080×1920, avec le mot `TEST` en Anton doré `#D9AE5C` qui entre par le bas en
ressort sur un fond sombre. Sors-le en `codex_test.mp4`.

S'il y arrive sans intervention, la configuration tient. S'il bloque, note où et
corrige.

---

## Ce que je veux en retour

1. La sortie de l'en-tête de `codex` après configuration
2. Le chemin du fichier de configuration écrit, et son contenu
3. Ce que tu as activé qui touche à la sécurité (réseau, approbations) et pourquoi
4. Ce qui manquait et que tu as installé
5. Le résultat du clip de test
6. Ce que tu n'as pas pu régler, s'il y a lieu — dis-le plutôt que de le contourner
