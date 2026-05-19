from cesar import chiffrer, dechiffrer

def enigma_chiffrer(msg,cles):
   
    msg_chiffrer=''
    for i, letter in enumerate(msg):
        index=i % 3
        msg_chiffrer += chiffrer(letter, cles[index])
    return msg_chiffrer

def enigma_dechiffrer(msg,cles):
    msg_dechiffrer=''
    for i, letter in enumerate(msg):
        index=i % 3
        msg_dechiffrer += dechiffrer(letter, cles[index])
    return msg_dechiffrer

