import unicodedata
from cesar import chiffrer, dechiffrer
from enigma import enigma_chiffrer, enigma_dechiffrer


def demander_cle_cesar():
    """Demande une clé entière pour César, redemande tant qu'invalide."""
    while True:
        cle_txt = input("Entrez la clé (un entier, ex: 42 ou -42) : ").strip()
        try:
            return int(cle_txt)
        except ValueError:
            print(f"'{cle_txt}' n'est pas un entier valide. Réessayez.")


def demander_cles_enigma():
    """Demande 3 clés entières pour Enigma (format 'a-b-c'), redemande tant qu'invalide."""
    while True:
        cles_txt = input("Entrez les 3 clés Enigma au format 'a-b-c' (ex: 7-16-9) : ").strip()
        parts = cles_txt.split("-")
        if len(parts) != 3:
            print("Il faut exactement 3 nombres séparés par '-'. Réessayez.")
            continue
        try:
            return tuple(int(x) for x in parts)
        except ValueError:
            print(f"'{cles_txt}' contient une valeur non entière. Réessayez.")


def normaliser(texte: str) -> str:
    """Met en minuscules + enlève les accents + enlève les espaces autour."""
    texte = texte.strip().lower()
    texte = unicodedata.normalize("NFKD", texte)
    texte = "".join(c for c in texte if not unicodedata.combining(c))
    return texte


def orchestrer():
    """Pose les questions à l'utilisateur et lance le chiffrement (César ou Enigma)."""

    # === ÉTAPE 1 : chiffrer ou déchiffrer ? ===
    action = ""
    while action not in ("chiffrer", "dechiffrer"):
        action = normaliser(input("Voulez-vous (chiffrer / dechiffrer) ? "))
        if action not in ("chiffrer", "dechiffrer"):
            print("Réponse invalide, tapez 'chiffrer' ou 'dechiffrer'.")

    # === ÉTAPE 2 : message tapé OU fichier texte ? ===
    source = ""
    while source not in ("message", "fichier"):
        source = normaliser(input("Source du texte (message / fichier) ? "))
        if source not in ("message", "fichier"):
            print("Réponse invalide, tapez 'message' ou 'fichier'.")

    # On récupère le texte
    if source == "message":
        texte = input("Entrez votre texte : ")
    else:
        chemin = input("Chemin du fichier (nom seul si même dossier) : ").strip()
        try:
            with open(chemin, "r", encoding="utf-8") as fio:
                texte = fio.read()
        except FileNotFoundError:
            print(f"Erreur : fichier '{chemin}' introuvable.")
            return

    # === ÉTAPE 2,5 : demander si cesar ou enigma ===
    mode = ""
    while mode not in ("cesar", "enigma"):
        mode = normaliser(input("Quel mode voulez-vous (cesar / enigma) ? "))
        if mode not in ("cesar", "enigma"):
            print("Réponse invalide, tapez 'cesar' ou 'enigma'.")

    # === ÉTAPE 3 : récupérer la clé et lancer l'algo ===
    if mode == "cesar":
        cle = demander_cle_cesar()
        if action == "chiffrer":
            resultat = chiffrer(texte, cle)
        else:
            resultat = dechiffrer(texte, cle)
    else:  # mode == "enigma"
        cles = demander_cles_enigma()
        if action == "chiffrer":
            resultat = enigma_chiffrer(texte, cles)
        else:
            resultat = enigma_dechiffrer(texte, cles)

    # === ÉTAPE 4 : afficher le résultat ===
    print("\n--- Résultat ---")
    print(resultat)
