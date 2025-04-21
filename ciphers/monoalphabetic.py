import string

def generate_substitution(key):
    key = ''.join(dict.fromkeys(key.upper()))
    alphabet = string.ascii_uppercase
    key_map = key + ''.join([c for c in alphabet if c not in key])
    return dict(zip(alphabet, key_map)), dict(zip(key_map, alphabet))

def encrypt(text, key):
    sub, _ = generate_substitution(key)
    return ''.join(sub.get(c.upper(), c) for c in text)

def decrypt(text, key):
    _, rev_sub = generate_substitution(key)
    return ''.join(rev_sub.get(c.upper(), c) for c in text)
