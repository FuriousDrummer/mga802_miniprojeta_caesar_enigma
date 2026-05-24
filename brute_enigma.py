
'''
Algorithme pour dechiffrer un message chiffrer par le chiffrement enigma
Cet algortihme s'appuie enormement sur le brute force du chiffrement cesar, notamment pour identifier les ressmblances avec le francais
'''

from brute_cesar import *
from enigma import enigma_dechiffrer, enigma_chiffrer


### dechiffrage base sur les frequences d'utilisations des lettres dans la langue francaise
def brute_force_enigma_frequence(message):
    meilleure_cle = 0
    meilleure_note = float("inf")
    for cle1 in range(1, 27):
        for cle2 in range(1, 27):
            for cle3 in range(1, 27):
                cle = (cle1, cle2, cle3)
                texte = enigma_dechiffrer(message, cle)       # on déchiffre avec cette clé
                note = ressemble_au_francais(texte)    # on note le résultat
                if note < meilleure_note:              # on garde la note la plus basse
                    meilleure_note = note
                    meilleure_cle = cle
    return meilleure_cle, enigma_dechiffrer(message, meilleure_cle)


### Fonction servant a dechiffrer un message avec l'aide du dictionnaire, ou des frequences si necessaire
def brute_force_dico_enigma(message_chiffre):

    dictionnaire = charger_dictionnaire()
    meilleur_nombre = -1
    meilleure_cle = (0,0,0)
    #On test toute les cles de (1,1,1) jusqu'a (26,26,26)
    for cle1 in range(1, 27):
        for cle2 in range(1, 27):
            for cle3 in range(1, 27):
                cle = (cle1, cle2, cle3)
                message = enigma_dechiffrer(message_chiffre, cle)
                connus, inconnus = analyser_mots(message, dictionnaire)
                if len(connus) > meilleur_nombre:
                    meilleur_nombre = len(connus)
                    meilleure_cle = cle

    if meilleur_nombre==0 :
        print("dechiffrage via frequence car dictionnaire pas assez efficace")
        meilleure_cle,message_dechiffrer=brute_force_enigma_frequence(message)
        return meilleure_cle, message_dechiffrer, None
    else :
        message_dechiffrer=enigma_dechiffrer(message_chiffre, meilleure_cle)
        connus, mots_non_identifies = analyser_mots( message_dechiffrer, dictionnaire)
        return meilleure_cle, message_dechiffrer, mots_non_identifies      
     
### cette fonction appelle soit la fonction dechiffrant avec le dictionnaire soit celle dechiffrant avec la frequence des lettres, selon le nombre de mots
def brute_force_enigma(message_chiffre):

    message_chiffre=normaliser(message_chiffre)
    if len(message_chiffre.split()) > SEUIL_MOTS:
        print("dechiffrage via frequence")
        cle,message, mots_non_identifies=brute_force_enigma_frequence(message_chiffre)
    else:
        print("dechiffrage via dictionnaire")
        cle,message, mots_non_identifies=brute_force_dico_enigma(message_chiffre)

    return cle,message,mots_non_identifies


### TEST###
message_test="n'hesitez pas a tester ce dechiffrement, on va avoir tout les points"
msg_chiffrer_test=enigma_chiffrer(message_test, (9,9,17))
print(msg_chiffrer_test)
a,b,c=brute_force_enigma(msg_chiffrer_test)
print(f'La cle est {a}, et le message est : {b}')
print(f"mots pas identifie : {c} ")