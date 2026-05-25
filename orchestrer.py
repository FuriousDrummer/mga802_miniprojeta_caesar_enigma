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

    # === ÉTAPE 3 : chiffrement (clé toujours demandée) ===
    if action == "chiffrer":
        if mode == "cesar":
            resultat = chiffrer(texte, demander_cle_cesar())
        else:
            resultat = enigma_chiffrer(texte, demander_cles_enigma())
        print("\n--- Résultat ---")
        print(resultat)
        return

    # === ÉTAPE 4 : déchiffrement -> connaît-on la clé ? ===
    connait_cle = ""
    while connait_cle not in ("oui", "non"):
        connait_cle = normaliser(input("Connaissez-vous la clé ? (oui / non) "))
        if connait_cle not in ("oui", "non"):
            print("Réponse invalide, tapez 'oui' ou 'non'.")

    # ÉTAPE 4a : clé connue -> déchiffrement classique
    if connait_cle == "oui":
        if mode == "cesar":
            resultat = dechiffrer(texte, demander_cle_cesar())
        else:
            resultat = enigma_dechiffrer(texte, demander_cles_enigma())
        print("\n--- Résultat ---")
        print(resultat)
        return

    # ÉTAPE 4b : clé inconnue -> brute-force
    if mode == "cesar":
        # import local pour éviter un import circulaire (brute_cesar importe orchestrer)
        from brute_cesar import brute_force_cesar
        cle, resultat, mots_non_identifies = brute_force_cesar(texte)
        print("\n--- Résultat ---")
        print(f"Clé trouvée   : {cle}")
        print(f"Déchiffrement : {resultat}")
        if mots_non_identifies:
            print(f"{len(mots_non_identifies)} mot(s) non identifié(s) : {mots_non_identifies}")
    else:
        from brute_enigma import brute_force_enigma
        cle, resultat, mots_non_identifies = brute_force_enigma(texte)
        print("\n--- Résultat ---")
        print(f"Clé trouvée   : {cle}")
        print(f"Déchiffrement : {resultat}")
        if mots_non_identifies:
            print(f"{len(mots_non_identifies)} mot(s) non identifié(s) : {mots_non_identifies}")
