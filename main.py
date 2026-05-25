from orchestrer import orchestrer
import argparse # pour utiliser argparse
from cesar import chiffrer, dechiffrer
from enigma import enigma_chiffrer, enigma_dechiffrer
from brute_cesar import brute_force_cesar
from brute_enigma import brute_force_enigma
import sys #pour comparer l'appel dans la console

def _parse_cle(texte : str):
	#converti la cle fournie en texte
	if "-" in texte.lstrip("-"):
		return tuple(int(x) for x in texte.split("-"))
	return int(texte)

def main():
	# si il n'y a pas d'arguments, le mode interactif est lance
	if len(sys.argv) == 1:
		orchestrer()
		return

	# sinon configuration de argparse
	parser = argparse.ArgumentParser(description="Outil de chiffrement César et Enigma.")

	# arguments principaux
	parser.add_argument("mode", choices=["cesar", "enigma"], help="Mode de chiffrement : cesar ou enigma")
	parser.add_argument("action", choices=["chiffrer", "dechiffrer", "bruteforce"], help="Action a effectuer : chiffrer, dechiffrer, bruteforce")
	parser.add_argument("message", help="Ecrire le texte a traiter ou le nom du fichier + -f")

	# arguments optionnels
	parser.add_argument("-c", choices=["chiffrer", "dechiffrer", "bruteforce"], help="Action a effectuer : chiffrer, dechiffrer, bruteforce")
	parser.add_argument("-f", "--fichier", action="store_true", help="Indique que l'argument 'texte' est un chemin de fichier.")

	try:
		args = parser.parse_args()
	except SystemExit:
		# argparse a détecté une erreur et essaie de quitter le script.
		print("La commande tapée est invalide ou incomplète.")
		print("Tapez 'python main.py -h' pour afficher le manuel d'aide complet.")
		sys.exit(1)  # On quitte le script proprement

	# check le fichier
	message = args.texte
	if args.fichier:
		try:
			with open(args.texte, "r", encoding="utf-8") as fio:
				message = fio.read()
		except FileNotFoundError:
			print(f"Erreur : fichier '{args.texte}' introuvable.")
			sys.exit(1)


	if args.action == "bruteforce":
			if args.mode == "cesar":
				cle, resultat, mots_non_identifies = brute_force_cesar(message)
			elif args.mode == "enigma":
				cle, resultat, mots_non_identifies = brute_force_enigma(message)
			print("\n--- Résultat Brute-Force ---")
			print(f"Clé trouvée   : {cle}")
			print(f"Déchiffrement : {resultat}")
			if any(mots_non_identifies):
				print(f"Mots non-identifiés : {mots_non_identifies}")



if __name__ == "__main__":
	main()























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
