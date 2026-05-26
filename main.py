'''
Ce programme permet de chiffrer, déchiffrer et bruteforce des messages avec le code césar ou un code énigma simplifié.
Il est possible d'appeler le programme pour avoir une interface ou appeler le fichier avec directement les arguments
pour une exécution plus rapide.
'''

from orchestrer import orchestrer, normaliser
import argparse # pour utiliser argparse
from cesar import chiffrer, dechiffrer
from enigma import enigma_chiffrer, enigma_dechiffrer
from brute_cesar import brute_force_cesar
from brute_enigma import brute_force_enigma
import sys #pour comparer l'appel dans la console

def main():
	"""
	Fonction principale qui analyse les arguments de la ligne de commande.
	"""

	# s'il n'y a pas d'arguments (juste le nom du script), le mode interactif est lancé
	if len(sys.argv) == 1:
		orchestrer()
		return

	# sinon la configuration de argparse est lancée
	parser = argparse.ArgumentParser(description="Outil de chiffrement César et Enigma.")

	# --- arguments principaux obligatoires ---
	parser.add_argument("mode", choices=["cesar", "enigma"], help="Mode de chiffrement : cesar ou enigma")
	parser.add_argument("action", choices=["chiffrer", "dechiffrer", "bruteforce"], help="Action a effectuer : chiffrer, dechiffrer, bruteforce")
	parser.add_argument("message", help="Ecrire le texte a traiter ou le nom du fichier + -f")

	# --- arguments optionnels ---
	parser.add_argument("-c", "--cle", help="La clé (ex: '-c 42' pour cesar, '-c 7-16-9' pour enigma). Requise sauf pour bruteforce.")
	parser.add_argument("-f", "--fichier", action="store_true", help="Indique que l'argument 'texte' est un chemin de fichier.")

	# interception d'erreurs
	try:
		args = parser.parse_args()
	except SystemExit:
		# interception d'une erreur d'entrée d'arguments
		# affiche un message explicatif puis quitte le script proprement
		print("La commande tapée est invalide ou incomplète.")
		print("Tapez 'python main.py -h' pour afficher le manuel d'aide complet.")
		return

	# --- traitement de l'entrée (texte ou fichier) ---
	message = args.message
	if args.fichier:
		try:
			with open(args.message, "r", encoding="utf-8") as fio:
				message = fio.read()
		except FileNotFoundError:
			print(f"Erreur : fichier '{args.message}' introuvable.")
			sys.exit(1)
		except UnicodeDecodeError:
			print(f"Erreur : le fichier '{args.message}' n'est pas un fichier texte (UTF-8) valide.")
			sys.exit(1)
	message = normaliser(message)

	# vérification de l'existence de la clé si l'action n'est pas un bruteforce
	# traitement de la clé en accord avec les choix
	if args.action in ["chiffrer", "dechiffrer"] and not args.cle:
		print("Erreur : La clé (-c) est requise pour chiffrer ou déchiffrer.")
		return
	elif args.mode == "cesar" and args.action in ["chiffrer", "dechiffrer"]:
		cle = args.cle
		try: # conversion de l'entrée STR en entier si possible, sinon retourner un message à l'utilisateur
			cle = int(cle)
		except ValueError:
			print(f"La clé contient une valeur non entière. Réessayez.")
			return
	elif args.mode == "enigma" and args.action in ["chiffrer", "dechiffrer"]:
		# séparation des 3 clés dans un tuple avec vérification de réussite, sinon retourner un message à l'utilisateur
		cle = args.cle
		cle = cle.split("-")
		if len(cle) != 3:
			print("Il faut exactement 3 clés séparées par '-'. Réessayez.")
			return
		try:
			cle = tuple(int(x) for x in cle)
		except ValueError:
			print(f"Les clés contiennent une valeur non entière. Réessayez.")
			return


	# --- execution de l'action dans le mode de chiffrement demandé ---
	if args.action == "bruteforce":
		if args.mode == "cesar":
			cle, resultat, mots_non_identifies = brute_force_cesar(message)
		else:
			cle, resultat, mots_non_identifies = brute_force_enigma(message)
		print("\n--- Résultat Brute-Force ---")
		print(f"Clé trouvée   : {cle}")
		print(f"Déchiffrement : {resultat}")
		if mots_non_identifies:
			print(f"Mots non-identifiés : {mots_non_identifies}")

	elif args.action == "chiffrer":
		if args.mode == "cesar":
			resultat = chiffrer(message, cle)
		else:
			resultat = enigma_chiffrer(message, cle)
		print(f"Le message chiffré est : {resultat}")

	elif args.action == "dechiffrer":
		if args.mode == "cesar":
			resultat = dechiffrer(message, cle)
		else:
			resultat = enigma_dechiffrer(message, cle)
		print(f"Le message déchiffré est : {resultat}")


if __name__ == "__main__":
	main()