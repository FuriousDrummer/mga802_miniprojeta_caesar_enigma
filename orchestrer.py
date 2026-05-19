import unicodedata
from cesar import chiffrer, dechiffrer


def demander_cle():
    """Demande une clé entière à l'utilisateur, redemande tant qu'invalide."""
    while True:
        cle_txt = input("Entrez la clé (un entier, ex: 42 ou -42) : ").strip()
        try:
            return int(cle_txt)
        except ValueError:
            print(f"'{cle_txt}' n'est pas un entier valide. Réessayez.")


def normaliser(texte: str) -> str:
    """Met en minuscules + enlève les accents + enlève les espaces autour."""
    texte = texte.strip().lower()
    texte = unicodedata.normalize("NFKD", texte)
    texte = "".join(c for c in texte if not unicodedata.combining(c))
    return texte


def orchestrer():
    """Pose les questions à l'utilisateur et lance le chiffrement César."""

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

    # === ÉTAPE 3 : récupérer la clé et lancer l'algo ===
    cle = demander_cle()
    if action == "chiffrer":
        resultat = chiffrer(texte, cle)
    else:
        resultat = dechiffrer(texte, cle)

    # === ÉTAPE 4 : afficher le résultat ===
    print("\n--- Résultat ---")
    print(resultat)
