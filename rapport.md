# Rapport — Mini-Projet A : Chiffrement de César & Enigma César

## 1. Structure du programme

Le code est découpé en **6 modules** aux responsabilités séparées, ce qui facilite la lecture, les tests et la collaboration via Git :

| Module | Rôle |
|---|---|
| `cesar.py` | Chiffrement/déchiffrement César (1 clé entière) |
| `enigma.py` | Chiffrement/déchiffrement Enigma César (3 clés cycliques) |
| `brute_cesar.py` | Recherche de clé César (fréquences + dictionnaire) |
| `brute_enigma.py` | Recherche de clé Enigma (26³ combinaisons) |
| `orchestrer.py` | Interface utilisateur en console + normalisation du texte |
| `main.py` | Point d'entrée (`python main.py`) |

**Dépendances** : `main → orchestrer → {cesar, enigma, brute_cesar}` ; `brute_enigma → {brute_cesar, enigma}`. Les modules de chiffrement (`cesar`, `enigma`) n'importent rien du projet : ils sont **réutilisables et testables isolément**.

**Choix de conception** :
- **Normalisation** centralisée dans `orchestrer.normaliser()` : minuscules + suppression des accents via `unicodedata.normalize("NFKD", ...)`. Le brute-force normalise systématiquement l'entrée pour garantir la cohérence du scoring.
- **Caractères hors alphabet** (ponctuation, espaces, chiffres) : conservés tels quels lors du chiffrement, ce qui préserve la lisibilité du texte chiffré.
- **Gestion de la clé** : `cesar` accepte n'importe quel entier (positif/négatif, modulo 26 implicite) ; `enigma` exige un tuple de 3 entiers, validé par `demander_cles_enigma()` qui redemande tant que la saisie est invalide.
- **Lecture fichier** : ouverture `with open(..., encoding="utf-8")` avec gestion d'`FileNotFoundError`.

## 2. Algorithmes

### 2.1 Chiffrement César
Décalage modulo 26 sur `string.ascii_lowercase`. Pour chaque lettre : `(position + clé) % 26`. Complexité **O(n)** où n = longueur du message.

### 2.2 Chiffrement Enigma César
Trois clés appliquées **cycliquement** (`i % 3`) en réutilisant `cesar.chiffrer()` lettre par lettre. Ce choix simplifie le code (pas de duplication) et garantit la cohérence sémantique entre les deux modes. Complexité **O(n)**.

### 2.3 Brute-force César — stratégie hybride
Deux scoreurs combinés selon un seuil `SEUIL_MOTS = 15` :

- **Texte long** → **analyse de fréquences (χ²)**. On déchiffre avec chacune des 26 clés, on calcule l'histogramme des lettres, et on compare à la distribution française de référence (E ≈ 14,7 %, A ≈ 7,6 %, …) via la statistique du khi-deux. La clé minimisant l'écart gagne. **Très rapide** (26 itérations, pas de chargement de dictionnaire).
- **Texte court** → **dictionnaire de mots français** (`mots_francais.txt`, ~30 000 mots chargés dans un `set` pour des lookups en O(1)). On compte les mots reconnus pour chaque clé ; la clé maximisant ce compte gagne. **Plus fiable** sur peu de lettres, où les fréquences ne sont pas significatives.
- **Repli** : si aucun mot n'est reconnu (texte court mais sans mot français complet), on bascule automatiquement sur les fréquences.

**Justification du seuil** : sous 15 mots, l'histogramme devient bruité (écart-type des fréquences observées trop grand vs la référence) et donne des faux positifs ; le dictionnaire prend le relais.

### 2.4 Brute-force Enigma César — 26³ = 17 576 combinaisons
Trois boucles imbriquées sur (cle1, cle2, cle3). Pour chaque triplet, on déchiffre puis on score avec **les mêmes fonctions** que pour César (`ressemble_au_francais`, `analyser_mots`) — ce qui évite toute duplication. Même logique hybride fréquences/dictionnaire selon `SEUIL_MOTS`.

**Coût dominant** : ce sont les 17 576 déchiffrements complets, chacun en O(n). Une optimisation possible (non retenue ici par souci de lisibilité) serait de déchiffrer **par position modulo 3** indépendamment (3 × 26 = 78 scorings au lieu de 17 576), exploitant le fait que les 3 clés agissent sur des positions disjointes.

## 3. Évaluation des performances

**Machine utilisée** : MacBook Pro (Mac17,9), Apple **M5 Pro** (15 cœurs : 10 perf. + 5 eff.), 24 Go RAM, macOS 26.5, Python 3.13.13.

**Méthodologie** : `timeit` avec un nombre de répétitions adapté au coût (100 pour César, 3–5 pour Enigma). Sorties `print()` redirigées pour ne pas biaiser la mesure. Moyenne par appel reportée.

```python
from timeit import timeit
timeit('brute_force_cesar(msg)', globals=globals(), number=100)
```

| Algorithme | Message | Stratégie | Temps moyen / appel | Combinaisons |
|---|---|---|---:|---:|
| Brute César | long (~ 50 mots) | fréquences | **0,92 ms** | 26 |
| Brute César | court (6 mots) | dictionnaire | **2,35 ms** | 26 |
| Brute Enigma | long | fréquences | **1,19 s** | 17 576 |
| Brute Enigma | court | dictionnaire | **0,13 s** | 17 576 |
| *(référence)* Chargement `mots_francais.txt` | — | — | 3,9 ms | — |

**Analyse** :
- **César/fréquences** (0,92 ms) bat **César/dictionnaire** (2,35 ms) d'un facteur ~2,5 : pas de chargement de fichier, pas de `split`/lookup par mot, juste un histogramme + 26 calculs de χ².
- Le **chargement du dictionnaire** (~30 000 mots dans un `set`) coûte 3,9 ms ; il est appelé **une seule fois** par brute-force, pas dans la boucle des 26 clés, donc son impact relatif diminue avec la taille du message.
- **Enigma/fréquences est ~1290× plus lent que César/fréquences**, au-delà du facteur théorique 676 (17 576 / 26). L'écart vient de `enigma_dechiffrer`, qui appelle `cesar.chiffrer/dechiffrer` **lettre par lettre** (un appel de fonction et un `import string` par caractère), alors que `cesar.dechiffrer` traite le message en une seule passe.
- **Enigma/dictionnaire (court) est ~10× plus rapide qu'Enigma/fréquences (long)** : malgré les mêmes 17 576 combinaisons, le message court contient bien moins de lettres à traiter par itération.
- Le bottleneck d'Enigma reste le **nombre de déchiffrements complets** ; une optimisation possible (non retenue ici pour préserver la lisibilité) serait d'exploiter le fait que les 3 clés agissent sur des positions disjointes (modulo 3), ramenant le problème à 3 × 26 = 78 sous-recherches indépendantes.

**Comparaison entre deux machines** — pour vérifier que l'algorithme se comporte de façon cohérente d'une machine à l'autre, le même benchmark (mêmes messages, mêmes appels, `number=100`) a été exécuté sur la machine d'un second membre de l'équipe :

| Test (mode dictionnaire, message court) | M5 Pro | `[Machine Victor — à préciser]` | Ratio |
|---|---:|---:|---:|
| `brute_force_cesar` | 2,64 ms | 16 ms | × 6,1 |
| `brute_force_enigma` | 227 ms | 985 ms | × 4,3 |

Le ratio est cohérent entre les deux tests (~5–6×), ce qui confirme que la différence vient bien du **matériel** (CPU, mémoire) et non d'un comportement asymétrique de l'algorithme.

## 4. Distribution des tâches

| Membre | Contributions |
|---|---|
| Nino MINASHVILI | brute-force César, orchestrer, rédaction du rapport |
| Kilian LEGAVRE | enigma, argparse, README |
| Victor Elmirzoiev Pradel De Lamaze | brute-force Enigma, tests unitaires, mesures de performance |

**Méthode collaborative** : chaque fonctionnalité a été développée sur une **branche dédiée** (`fonctions_mise_en_page`, `cesar_dechiffrer`, `orchestre-du-debut`, `enigma`, `branche-des-tests`, `argparse_integration`) puis intégrée à `main` via **pull request** (6 PR mergées, #1 à #6). Les messages de commit sont descriptifs en français. L'historique Git (`git log --author=…`) trace l'avancée de l'équipe.
