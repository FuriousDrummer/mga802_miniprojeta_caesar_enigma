"""
Brute-force du chiffrement de César.

On ne connaît pas la clé : on essaie de la retrouver. Deux stratégies, choisies
selon la longueur du texte :
- Texte long  : on déchiffre avec chaque clé et on garde celui qui RESSEMBLE le
  plus à du français (fréquence des lettres). Rapide et fiable sur un long texte.
- Texte court : on déchiffre avec chaque clé et on garde celui qui contient le
  plus de VRAIS MOTS français (dictionnaire). Plus fiable quand il y a peu de
  lettres.
"""

import string

from cesar import dechiffrer
from orchestrer import normaliser

alphabet = string.ascii_lowercase  # 'abcdefghijklmnopqrstuvwxyz'

# En dessous de ce nombre de mots, on utilise le dictionnaire ; au-dessus, les
# fréquences de lettres suffisent.
SEUIL_MOTS = 15

# Fréquence habituelle de chaque lettre en français, en pourcentage (a -> z).
frequences_fr = [
    7.636, 0.901, 3.260, 3.669, 14.715, 1.066, 0.866, 0.737, 7.529,
    0.613, 0.074, 5.456, 2.968, 7.095, 5.378, 3.021, 1.362, 6.553,
    7.948, 7.244, 6.311, 1.628, 0.114, 0.387, 0.308, 0.136,
]


def calculer_histogramme(message):
    """Compte combien de fois chaque lettre (a -> z) apparaît dans le message.

    Retourne une liste de 26 nombres : la case 0 = nombre de 'a', la case 1 =
    nombre de 'b', etc.
    """
    histogramme = [0] * 26
    for lettre in message:
        if lettre in alphabet:
            position = alphabet.find(lettre)   # 'a' -> 0, 'b' -> 1, ...
            histogramme[position] += 1
    return histogramme


def ressemble_au_francais(texte):
    """Donne une note au texte : plus elle est BASSE, plus ça ressemble au français.

    On compte les lettres du texte, puis on regarde à quel point cela s'écarte
    des fréquences habituelles du français (test du khi-deux).
    """
    histogramme = calculer_histogramme(texte)
    total = sum(histogramme)
    if total == 0:                 # aucune lettre dans le texte
        return float("inf")        # "infini" = le pire score possible

    note = 0
    for i in range(26):
        observe = histogramme[i]                   # ce qu'on a vraiment
        attendu = frequences_fr[i] / 100 * total   # ce qu'on aurait en français
        note += (observe - attendu) ** 2 / attendu # on calcul l'écart 
    return note


def brute_force_frequences(message):
    """Essaie les 26 clés et garde celle dont le déchiffrement ressemble le plus au français.

    Retourne (meilleure_cle, message_dechiffre).
    """
    meilleure_cle = 0
    meilleure_note = float("inf")
    for cle in range(26):
        texte = dechiffrer(message, cle)       # on déchiffre avec cette clé
        note = ressemble_au_francais(texte)    # on note le résultat
        if note < meilleure_note:              # on garde la note la plus basse
            meilleure_note = note
            meilleure_cle = cle
    return meilleure_cle, dechiffrer(message, meilleure_cle)


def charger_dictionnaire():
    """Charge la liste de mots français du fichier dans un set (recherche rapide)."""
    dictionnaire = set()
    with open("mots_francais.txt", encoding="utf-8") as fichier:
        for ligne in fichier:
            dictionnaire.add(ligne.strip())   # .strip() enlève le saut de ligne
    return dictionnaire


def analyser_mots(texte, dictionnaire):
    """Sépare les mots du texte en deux listes : ceux connus du dico, et les autres."""
    texte = texte.replace("'", " ")   # "l'ami" devient "l ami"
    connus = []
    inconnus = []
    for mot in texte.split():         # découpe le texte sur les espaces
        # on garde seulement les lettres du mot (on retire ! , . etc.)
        mot_propre = ""
        for lettre in mot:
            if lettre in alphabet:
                mot_propre += lettre
        if mot_propre == "":          # le "mot" n'avait aucune lettre
            continue
        if mot_propre in dictionnaire:
            connus.append(mot_propre)
        else:
            inconnus.append(mot_propre)
    return connus, inconnus


def brute_force_dictionnaire(message):
    """Essaie les 26 clés et garde celle qui donne le plus de vrais mots français.

    Retourne (meilleure_cle, message_dechiffre, mots_non_identifies).
    Si aucune clé ne donne de mot connu, on se rabat sur les fréquences.
    """
    dictionnaire = charger_dictionnaire()

    # On cherche la clé qui donne le plus de mots reconnus.
    meilleure_cle = 0
    meilleur_nombre = -1
    for cle in range(26):
        texte = dechiffrer(message, cle)
        connus, inconnus = analyser_mots(texte, dictionnaire)
        if len(connus) > meilleur_nombre:
            meilleur_nombre = len(connus)
            meilleure_cle = cle

    # Aucun mot français trouvé : le dictionnaire n'aide pas, on passe aux fréquences.
    if meilleur_nombre == 0:
        cle, dechiffre = brute_force_frequences(message)
        print("dico n'a pas marché, on utilise fréquence. ")
        return cle, dechiffre, None #None car la fonction brute_force_frequences ne renvoie que 2 reusltats (pas de mots non identifiés)

    # On déchiffre avec la meilleure clé et on note les mots non reconnus.
    dechiffre = dechiffrer(message, meilleure_cle)
    connus, mots_non_identifies = analyser_mots(dechiffre, dictionnaire)
    print()
    print()
    print()
    print("dico a bien marché")
    return meilleure_cle, dechiffre, mots_non_identifies


def brute_force_cesar(message_chiffre):
    """Retrouve la clé d'un message chiffré par César.

    - Plus de mots dans message que SEUIL_MOTS -> on utilise les fréquences de lettres.
    - SEUIL_MOTS mots ou moins  -> on utilise le dictionnaire ->  Retourne (meilleure_cle, message_dechiffre, mots_non_identifies).
    
    Retourne (meilleure_cle, message_dechiffre, mots_non_identifies).
    (mots_non_identifies vaut None quand on a utilisé les fréquences.)
    """
    message = normaliser(message_chiffre)

    if len(message.split()) > SEUIL_MOTS:
        cle, dechiffre = brute_force_frequences(message)
        return cle, dechiffre, None
    
    return brute_force_dictionnaire(message)

"""DEMO EN LANÇANT LE FICHIER :)"""
if __name__ == "__main__":
    # Démonstration : on chiffre une phrase, puis on retrouve la clé sans la donner.
    from cesar import chiffrer

    exemple = "bonjour, qu'est ce que, tu brute force attends un mot identifie quoi aesrdtfyguhj "
    chiffre = chiffrer(exemple, 5)
    cle_trouvee, dechiffre, mots_non_identifies = brute_force_cesar(chiffre)

    print(f"Message chiffré : {chiffre}")
    print(f"Clé trouvée     : {cle_trouvee}")
    print(f"Déchiffrement   : {dechiffre}")
    if mots_non_identifies:
        print(f"{len(mots_non_identifies)} mot(s) non identifié(s) : {mots_non_identifies}")
