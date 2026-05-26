# MGA802 — Mini-Projet A : Chiffrement de César

## Le code
Ce script est un outil interactif développé dans le but de pouvoir chiffrer, déchiffrer et déchiffrer sans clé un message.
Pour se faire, le programme se base sur 2 méthode historiques : le code **César** et une version simplifiée de la machine **Enigma**.

## Méthodes : 

Cesar : 1 clé, décalage de rangs dans l'alphabet

Enigma : 3 clés, décalage cyclique dans l'alphabet

## Fonctions

Le code, en plus de pouvoir effectuer les 3 action citées précédemment, prend en charge les fichiers texte.

- **Chiffrage :** Chiffrage du message avec la méthode et la clé fournie
- **Déchiffrage :** Déchiffrage du message avec la méthode et la clé fournie
- **Bruteforce :** Déchiffrage du message *sans avoir la clé* grâce à 2 méthodes : 
  - Teste toutes les clés possibles et confronte les résultats à un dictionnaire intégré `mots_francais.txt` pour identifier les vrais mots
  - Approche statistique en analysant la fréquence d'apparition des lettres, s'appuyant sur les probabilités naturelles de la langue française pour retrouver le message clair d'origine

## Installation

Téléchargez ou clonez l'ensemble des fichiers du projet dans un même dossier :
   * `main.py` (Point d'entrée)
   * `orchestrer.py` (Gestion de l'interface utilisateur)
   * `cesar.py` & `enigma.py` (Algorithmes de chiffrement)
   * `brute_cesar.py` & `brute_enigma.py` (Algorithmes de cassage)
   * `mots_francais.txt` (Dictionnaire de référence)

## Utilisation

#### 1. Mode Interactif (Guidé)
Idéal pour une utilisation pas-à-pas. Lancez simplement le script sans aucun argument, et laissez-vous guider par les menus textuels de la console : 

`python main.py`


#### 2. Mode Ligne de commande

Il est également possible d'appeler les fonctionnalités du script directement dans la console en utilisant : 

`python main.py <mode> <action> "<message>" [-c CLE] [-f]`

`mode` : cesar ou enigma

`action` : chiffrer, dechiffrer, ou bruteforce

`message` : Le texte à traiter (ou le nom du fichier si l'option -f est utilisée)

`-c` + `CLE` : La clé de chiffrement (ex: -c 42 pour César, -c 7-16-9 pour Enigma). Requise sauf pour la fonction bruteforce.

`-f` : (Optionnel) Indique que le paramètre message est un chemin vers un fichier texte.

Pour plus d'informations, veuillez entrer  `python main.py -h`

# Choix de conception

- **Normalisation du texte :** Normalisation des lettres dans les messages (pas d'accents, tout en minuscule) dans le but d'avoir un traitement plus fluide et éviter des erreurs lors de l'analyse fréquentielle ou de correspondance avec le dictionnaire.
- **Découplage du code :** Séparation de la partie interactive du code dans `orchestrer.py`. Permet d'alléger le fichier `main.py` qui appelera simplement l'interface utilisateur guidée si besoin.
- **Point d'entrée hybride :** Fonction main composée de l'appel de `orchester()` pour le modèle interactif et de la série d'arguments `argparse`. Permet de basculer entre un mode interactif guidé et un mode CLI performant au besoin.
- **Découplage des types d'action et de chiffrement :** Les 2 types de chiffrement (césar et enigma) sont séparés dans leur fichier respectif `cesar.py` & `enigma.py` où enigma utilise des fonctions de césar pour optimiser la réutilisation de fonction. Il est de même pour les fichiers contenant les procédures de bruteforce `brute_cesar.py` & `brute_enigma.py`.

# Auteurs

- Victor ELMIRZOIEV PRADEL DE LAMAZE
- Kilian LEGAVRE
- Nino MINASHVILI