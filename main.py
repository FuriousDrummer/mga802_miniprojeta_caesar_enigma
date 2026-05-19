""" Travail de chef d'orchestre

demander si l'utilisateur veut encoder ou décoder

demander si l'utilisateur veut écrire son message ou si il a un fichier text
    si son message :
        transformer son message en liste de de str de travail
    si fichier :
        transformer le fichiers en liste de str de travail

si c'est encoder :
    demander la clé que l'utilisateur veut tuiliser
si c'est décoder :
    demander si il a le code ou si il faut décoder de manière brulate

    """
import unicodedata

from cesar import chiffrer, dechiffrer
from enigma import enigma_chiffrer, enigma_dechiffrer


# Remarque : chiffrer(), dechiffrer() et brute_force_cesar() sont définies dans d'autres fichiers propres 
# plus haut dans ce module (ou importées) par le reste de l'équipe.
# L'orchestrateur ci-dessous se contente de les appeler avec les bons arguments.


def demander_cle():
    """Demande une clé entière à l'utilisateur.

    Retourne :
        int : la clé saisie si elle est valide
        None : si la saisie n'est pas un entier (on arrêtera l'orchestrateur)
    """
    cle_txt = input("Entrez la clé (un entier, ex: 42 ou -42) : ").strip()
    try:
        return int(cle_txt)
    except ValueError:
        print(f"'{cle_txt}' n'est pas un entier valide. Réessayez.")



def normaliser(texte: str) -> str:
      """Met en minuscules, enlève les accents et les espaces autour."""
      # 1. Mettre en minuscules + enlever espaces début/fin
      texte = texte.strip().lower()
      # 2. Décomposer chaque lettre accentuée en (lettre + accent séparé)
      #    Ex: "é" → "e" + "´"
      texte = unicodedata.normalize("NFKD", texte)
      # 3. Garder uniquement les caractères qui ne sont PAS des accents
      texte = "".join(c for c in texte if not unicodedata.combining(c))
      return texte


def orchestrer():
    """Pose les questions à l'utilisateur et lance le chiffrement César."""

    # === ÉTAPE 1 : chiffrer ou déchiffrer ? ===
    # On boucle tant que la réponse n'est pas valide pour éviter de planter.
    action = ""
    while action not in ("chiffrer", "dechiffrer"):
        action = normaliser(input("Voulez-vous (chiffrer / dechiffrer) ? ").strip().lower())
        if action not in ("chiffrer", "dechiffrer"):
            print("Réponse invalide, tapez 'chiffrer' ou 'dechiffrer'.")

    # === ÉTAPE 2 : message tapé OU fichier texte ? ===
    source = ""
    while source not in ("message", "fichier"):
        source = normaliser(input("Source du texte (message / fichier) ? ").strip().lower())
        if source not in ("message", "fichier"):
            print("Réponse invalide, tapez 'message' ou 'fichier'.")

    # On récupère le texte sous forme de str (les fonctions chiffrer/dechiffrer
    # attendent une str, pas une liste).
    if source == "message":
        # Saisie directe au clavier.
        texte = input("Entrez votre texte : ")
        
    else:
        # Lecture depuis un fichier texte (UTF-8 par défaut).
        chemin = input("Chemin du fichier à lire : " \
        "Mettre juste le nom du fichier si dans le meme dossier").strip()
        try:
            with open(chemin, "r", encoding="utf-8") as fio:
                texte = fio.read()
        except FileNotFoundError:
            print(f"Erreur : fichier '{chemin}' introuvable.")
            return


    # === ÉTAPE 3 : récupérer la clé OU déclencher le brute-force ===
    if action == "chiffrer":
        # Pour chiffrer, on a forcément besoin d'une clé.
        cle = demander_cle()
        resultat = chiffrer(texte, cle)

    else:
        # Pour déchiffrer : soit l'utilisateur a la clé, soit on brute-force.
        choix = ""
        while choix not in ("cle", "brute"):
            choix = normaliser(input("Avez-vous la clé ? Entrez 'cle' ou 'brute') ").strip().lower())
            if choix not in ("cle", "brute"):
                print("Réponse invalide, tapez 'cle' ou 'brute'.")

        if choix == "cle":
            cle = demander_cle()
            resultat = dechiffrer(texte, cle)
        else:
            # Brute-force : teste les 26 clés possibles (fait par l'équipe).
            resultat = brute_force_cesar(texte)

    # === ÉTAPE 4 : afficher le résultat ===
    print("\n--- Résultat ---")
    print(resultat)


if __name__ == "__main__":
    # Permet de lancer l'orchestrateur directement avec : python cesar.py
    orchestrer()


"""
MGA802 — Mini-Projet A : Chiffrement de César
Squelette de départ pour votre équipe.
"""
"""import argparse
import unicodedata  # Pour gérer et supprimer les accents des caractères

def formater_le_message(message_brut = "Vini, Vidi, Vici !"):
    '''
    Formate le mot : le met en minuscule et retire tous les accents.
    '''
	# Le mot est passé tout en majuscules
    message_traite = message_brut.lower()

    # unicodedata.normalize('NFD', mot) sépare les caractères de base et leurs accents
    # .encode('ascii', 'ignore') convertit en ASCII et supprime les accents ainsi isolés
    # .decode('utf-8') reconvertit le tout en chaîne de caractères classique
    message_traite = unicodedata.normalize('NFD', message_traite) \
        .encode('ascii', 'ignore') \
        .decode('utf-8')
    return message_traite
"""
"""
def chiffrer(message: str, cle: int):
	# TODO: retourner la chaîne chiffrée (type str).
	# Exigences visibles dans tests/test_caesar.py :
	# - test_cesar_officiel_cle_42
	# - test_cesar_officiel_cle_neg_42
	# - test_cesar_cle_zero_identite
	# Exemples attendus par les tests :
	# - chiffrer("Veni, vidi, vici!", 42) -> "Ludy, lyty, lysy!"
	# - chiffrer("Veni, vidi, vici!", -42) -> "Foxs, fsns, fsms!"
	# - chiffrer("Tout pareil.", 0) -> "Tout pareil."
	pass


def dechiffrer(message: str, cle: int):
	# TODO: retourner la chaîne déchiffrée (type str).
	# Exigence visible dans tests/test_caesar.py :
	# - test_cesar_round_trip
	# Le test vérifie que dechiffrer(chiffrer(msg, 7), 7) == msg.
	pass


def enigma_chiffrer(message: str, cles):
	# TODO: retourner la chaîne chiffrée Enigma César (type str).
	# Exigence visible dans tests/test_caesar.py :
	# - test_enigma_officiel_maison
	# Exemple attendu par le test :
	# - enigma_chiffrer("MAISON", (7, 16, 9)) -> "TQRZEW"
	pass


def _parse_cle(texte: str):
	'''Convertit l'argument --cle en clé utilisable.

	Cette fonction analyse la clé fournie par l'utilisateur en ligne de commande
	et la transforme en type Python approprié :
	- César           : un entier, ex. "42" ou "-42"
	- Enigma César    : trois entiers séparés par des tirets, ex. "7-16-9"

	Paramètre :
		texte (str) : la chaîne saisie par l'utilisateur après --cle.

	Retour :
		int : une clé entière pour César
		tuple : un tuple de 3 entiers pour Enigma César

	Exemple :
		_parse_cle("42") → 42 (int)
		_parse_cle("7-16-9") → (7, 16, 9) (tuple)
	'''
	# Vérifier s'il y a un tiret dans la clé (sauf si c'est juste un signe négatif).
	# lstrip("-") enlève tous les tirets au début, pour distinguer :
	#   "-42" (entier négatif, pas de tiret après le signe)
	#   "7-16-9" (trois nombres séparés par des tirets)
	if "-" in texte.lstrip("-"):
		# Si oui, c'est une clé Enigma César : on coupe au niveau du "-" et on convertit en entiers.
		return tuple(int(x) for x in texte.split("-"))
	# Sinon, c'est une clé César simple : on convertit en entier.
	return int(texte)

def main(argv=None):
	'''Point d'entrée principal du programme en ligne de commande.

	Cette fonction :
	1. Parse les arguments saisis par l'utilisateur (action, message, clé)
	2. Convertit la clé en type approprié (int ou tuple)
	3. Appelle la fonction correspondante (chiffrer, dechiffrer ou enigma_chiffrer)
	4. Affiche le résultat

	Paramètre :
		argv (list ou None) : si None, utilise sys.argv (arguments de la console).
		                      si list, utilise les arguments fournis (utile pour les tests).

	Exemples d'utilisation en terminal :
		python main.py chiffrer "Veni, vidi, vici!" --cle 42
		python main.py dechiffrer "Ludy, lyty, lysy!" --cle 42
		python main.py enigma "MAISON" --cle 7-16-9
	'''
	# === ÉTAPE 1 : Créer et configurer le parseur d'arguments ===
	# argparse est un module qui aide à gérer les arguments en ligne de commande.
	# ArgumentParser crée un analyseur personnalisé pour notre programme.
	parser = argparse.ArgumentParser(
		description="Mini-Projet A : chiffrement de César / Enigma César.")

	# === ÉTAPE 2 : Définir les arguments attendus ===

	# Argument positionnel "action" : l'opération à effectuer.
	# - Obligatoire (pas de -- devant)
	# - Doit être l'une des valeurs listées dans "choices"
	parser.add_argument(
		"action",
		choices=["chiffrer", "dechiffrer", "enigma"],
		help="Opération à effectuer (chiffrer, dechiffrer ou enigma).")

	# Argument positionnel "message" : le texte à traiter.
	# - Obligatoire
	# - C'est la chaîne que nous allons chiffrer ou déchiffrer
	parser.add_argument(
		"message",
		help="Texte à traiter (mettez-le entre guillemets).")

	# Argument optionnel "--cle" (abréviation "-c") : la clé de chiffrement.
	# - Obligatoire via required=True
	# - Peut être un entier (César) ou trois entiers séparés par des tirets (Enigma César)
	parser.add_argument(
		"-c", "--cle", required=True,
		help="Clé : un entier (ex. '42') ou 'a-b-c' (ex. '7-16-9') pour Enigma.")

	# === ÉTAPE 3 : Analyser les arguments ===
	# parse_args() transforme les arguments en un objet "Namespace" avec des attributs.
	# Si argv=None, il lit automatiquement depuis la ligne de commande.
	# Sinon, il utilise la liste fournie.
	args = parser.parse_args(argv)

	# Maintenant, on peut accéder aux arguments via :
	# - args.action (ex. "chiffrer")
	# - args.message (ex. "Veni, vidi, vici!")
	# - args.cle (ex. "42" ou "7-16-9", toujours en chaîne de caractères)

	# === ÉTAPE 4 : Convertir la clé (texte) en type approprié ===
	# _parse_cle() transforme la clé en int (César) ou tuple (Enigma).
	cle = _parse_cle(args.cle)

	# === ÉTAPE 5 : Choisir et exécuter l'opération ===
	# Selon l'action, on appelle la fonction appropriée.
	# (Une fois que chiffrer / dechiffrer / enigma_chiffrer seront implémentées,
	#  ces appels retourneront le résultat du chiffrement/déchiffrement.)

	if args.action == "chiffrer":
		# L'utilisateur veut chiffrer : on appelle chiffrer()
		resultat = chiffrer(args.message, cle)
	elif args.action == "dechiffrer":
		# L'utilisateur veut déchiffrer : on appelle dechiffrer()
		resultat = dechiffrer(args.message, cle)
	else:  # args.action == "enigma"
		# L'utilisateur veut utiliser Enigma César : on appelle enigma_chiffrer()
		resultat = enigma_chiffrer(args.message, cle)

	# === ÉTAPE 6 : Afficher le résultat ===
	# print() affiche le résultat à l'écran pour que l'utilisateur le voie.
	print(resultat)
	
	# TODO : Une fois les fonctions de base implémentées, vous pourrez :
	# - Ajouter des options pour lire/écrire depuis des fichiers
	# - Implémenter le mode brute-force
	# - Ajouter d'autres fonctionnalités


if __name__ == "__main__":
	# Ce bloc s'exécute SEULEMENT si ce fichier est lancé directement depuis le terminal.
	# Exemple : python main.py chiffrer "Veni" --cle 42
	#
	# Il ne s'exécute PAS si on fait "import main" depuis un autre fichier Python.
	# Cela permet d'utiliser le code de main.py dans d'autres projets sans lancer main().
	# 
	# Pour les tests : pytest importe ce fichier mais ne lance pas main()
	# (car __name__ ne vaut pas "__main__" lors d'un import).
	main()

"""
