from cesar import chiffrer, dechiffrer

def enigma_chiffrer(msg,cles):
   
    msg_chiffrer=''
    for i, letter in enumerate(msg):
        index=i % 3
        msg_chiffrer += chiffrer(letter, cles[index])
    return msg_chiffrer

def enigma_dechiffrer(msg,cles):

    msg_dechiffrer=''
    for i in range(len(msg)):
        index = i % len(cles)
        msg_dechiffrer -= dechiffrer(msg[i], cles[index])
    return msg_dechiffrer

