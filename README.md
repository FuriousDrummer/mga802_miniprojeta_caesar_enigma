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
- **Bruteforce :** Déchiffrage du message grâce à une base de mots et de la fréquence d'apparition des lettres dans la langue française.

## Utilisation

Pour utiliser ce code, il suffit de lancer le fichier `main.py` et de suivre les instructions.


Il est également possible d'appeler les fonctionnalités du script directement dans la console en utilisant : 
`python main.py "méthode de chiffrement" "action à réaliser" "message" -c "clé -f`.  
`-c "clé"` étant optionnel lors d'un bruteforce.
`-f ` signifiant au programme que le message entré est le nom du fichier texte à chiffrer.

Pour plus d'informations, veuillez entrer  `python main.py -h`

# Auteurs

- Victor ELMIRZOIEV PRADEL DE LAMAZE
- Kilian LEGAVRE
- Nino MINASHVILI

# Choix de conception

- Normalisation des lettres dans les messages (pas d'accents, tout en minuscule) dans le but d'avoir un traitement plus fluide.
- Séparation de la partie interactive du code dans `orchestrer.py` dans le but d'alléger le `main.py`.
- Fonction main composée de l'appel de `orchester()` pour le modèle interactif et de la série d'arguments `argparse` dans le but de supporter une utilisation du script interactive ou rapide.