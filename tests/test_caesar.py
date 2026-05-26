"""Tests pour le Mini-Projet A.

Ce fichier contient les chaînes de test officielles + quelques cas
limites. Ajoutez vos propres tests au fur et à mesure.

Pour lancer les tests :
    pip install pytest
    pytest -v
"""
import sys
from pathlib import Path

# Permet d'importer main.py depuis le dossier parent
sys.path.insert(0, str(Path(__file__).parent.parent))
from cesar import chiffrer, dechiffrer
from enigma import enigma_chiffrer, enigma_dechiffrer
from brute_enigma import brute_force_enigma
from brute_cesar import brute_force_cesar
from orchestrer import normaliser


# ---------- Chaînes de test officielles — César (spec §7) ----------

def test_cesar_officiel_cle_42():
    assert chiffrer("veni, vidi, vici!", 42) == "ludy, lyty, lysy!"


def test_cesar_officiel_cle_neg_42():
    assert chiffrer("veni, vidi, vici!", -42) == "foxs, fsns, fsms!"


# ---------- Chaîne de test officielle — Enigma César (spec §2.6) ----------

def test_enigma_officiel_maison():
    assert enigma_chiffrer("maison", (7, 16, 9)) == "tqrzew"


# ---------- Cas standards  ----------

def test_cesar_round_trip():
    """Chiffrer puis déchiffrer doit redonner le message original."""
    msg = "bonjour le monde !"
    assert dechiffrer(chiffrer(msg, 7), 7) == msg

def test_enigma_phrase():
    msg = "bonjour le monde !"
    assert enigma_dechiffrer(enigma_chiffrer(msg, (10,18,34)), (10,18,34)) == msg

def test_cesar_cle_zero_identite():
    """Une clé de 0 ne doit rien changer."""
    assert chiffrer("tout pareil.", 0) == "tout pareil."

def test_brute_force_cesar_mot():
    assert brute_force_cesar(chiffrer("maison", 42)) == (16,"maison",[])

def test_brute_force_cesar_phrase():
    assert brute_force_cesar(chiffrer("le renard attaque les poules", 42)) == (16,"le renard attaque les poules",[])

def test_brute_force_enigma():
    assert brute_force_enigma(enigma_chiffrer("maison", (7, 16, 9))) == ((7, 16, 9), "maison", [])

def test_brute_force_enigma_phrase():
    assert brute_force_enigma(enigma_chiffrer("le loup mange les renardeaux", (7, 16, 19))) == ((7, 16, 19), "le loup mange les renardeaux", ['renardeaux'])

def test_enigma_trois_cles():
    #On teste que la fonction retourne un message d'erreur si on mets plus de 3 clefs
    assert enigma_chiffrer("maison", (7, 16, 9, 18,226)) == "Clefs invalides, il faut trois clefs"

def test_cesar_cle_invalide():
    #On teste que la fonction retourne un message d'erreur si on mets une clef qui n'est ps un entier
    assert chiffrer("erreur.", 'bonjour') == "Erreur ! Il ne faut qu'une clef et elle doit etre un nombre"

def test_maj_et_accents():
    '''On mets un message avec des majuscules et ccaracteres speciaux et un message normaliser
    Puis on verifie que les deux ont le même chiffrement
    '''
    msg=normaliser("Je mets un mesSage Avec des caractéres Speciaux à tester même")
    msg_normal="je mets un message avec des caracteres speciaux a tester meme"
    a=chiffrer(msg_normal, 42)
    assert chiffrer(msg, 42) == a

def test_grandes_cles_enigma():
    '''On test des clefs de grandes taille positves et negatives'''
    assert enigma_chiffrer("maison", (26007, 1316, -2617)) == "tqrzew"

def test_chaine_vide():
    '''Cas limite : une chaîne vide doit rester vide après chiffrement (César et Enigma).'''
    assert chiffrer("", 5) == ""
    assert dechiffrer("", 5) == ""
    assert enigma_chiffrer("", (7, 16, 9)) == ""
    assert enigma_dechiffrer("", (7, 16, 9)) == ""


