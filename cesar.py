def chiffrer (message_brut = "veni, vidi, vici!", cle = 42) :
    import string
    alphabet = string.ascii_lowercase
    # 'abcdefghijklmnopqrstuvwxyz'

    message_traite = ''
    for letter in message_brut :
        if letter in alphabet :
            position_initiale = alphabet.find(letter)
            position_finale = (position_initiale + cle) % len(alphabet)
            message_traite += alphabet[position_finale]
        else :
            message_traite += letter

    return message_traite

def dechiffrer (message_brut = "veni, vidi, vici!", cle = 42) :
    import string
    alphabet = string.ascii_lowercase
    # 'abcdefghijklmnopqrstuvwxyz'

    message_traite = ''
    for letter in message_brut :
        if letter in alphabet :
            position_initiale = alphabet.find(letter)
            position_finale = (position_initiale - cle) % len(alphabet)
            message_traite += alphabet[position_finale]
        else :
            message_traite += letter

    return message_traite