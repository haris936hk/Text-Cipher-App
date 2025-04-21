def repeat_key(text, key):
    key = key.upper()
    return (key * (len(text) // len(key))) + key[:len(text) % len(key)]

def encrypt(text, key):
    key = repeat_key(text, key)
    result = ""
    for i, char in enumerate(text):
        if char.isalpha():
            offset = ord('A') if char.isupper() else ord('a')
            key_char = ord(key[i].upper()) - ord('A')
            result += chr((ord(char) - offset + key_char) % 26 + offset)
        else:
            result += char
    return result

def decrypt(text, key):
    key = repeat_key(text, key)
    result = ""
    for i, char in enumerate(text):
        if char.isalpha():
            offset = ord('A') if char.isupper() else ord('a')
            key_char = ord(key[i].upper()) - ord('A')
            result += chr((ord(char) - offset - key_char + 26) % 26 + offset)
        else:
            result += char
    return result
