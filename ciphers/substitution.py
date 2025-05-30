def encrypt(text, key):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = key.upper()
    
    result = ""
    for char in text:
        if char.isalpha():
            
            if char.isupper():
                pos = ord(char) - ord('A')
                result += key[pos]
            else:
                pos = ord(char.upper()) - ord('A')
                result += key[pos].lower()
        else:
            result += char
    return result

def decrypt(text, key):
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = key.upper()
    
    
    reverse_key = [''] * 26
    for i, char in enumerate(key):
        reverse_key[ord(char) - ord('A')] = alphabet[i]
    
    result = ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                pos = ord(char) - ord('A')
                result += reverse_key[pos]
            else:
                pos = ord(char.upper()) - ord('A')
                result += reverse_key[pos].lower()
        else:
            result += char
    return result