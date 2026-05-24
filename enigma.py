from cesar import chiffrer, dechiffrer

def enigma_chiffrer(msg,cles):
    if len(cles)!=3 :
        return "Clefs invalides, il faut trois clefs"
    if type(cles[0]) != int or type(cles[1]) != int or type(cles[2]) != int:
        return "Clefs invalides, les clefs doivent être des nombres"
    else:
        msg_chiffrer=''
        for i, letter in enumerate(msg):
            index=i % 3
            msg_chiffrer += chiffrer(letter, cles[index])
        return msg_chiffrer

def enigma_dechiffrer(msg,cles):
    if len(cles)!=3 :
        return "Clefs invalides, il faut trois clefs"
    if type(cles[0]) != int or type(cles[1]) != int or type(cles[2]) != int:
        return "Clefs invalides, les clefs doivent être des nombres"
    else:
        msg_dechiffrer=''
        for i, letter in enumerate(msg):
            index=i % 3
            msg_dechiffrer += dechiffrer(letter, cles[index])
        return msg_dechiffrer


