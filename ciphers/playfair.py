import string

def to_lowercase(text: str) -> str:
    return text.lower()

def remove_spaces(text: str) -> str:
    return ''.join(c for c in text if c != ' ')

def digraphs(text: str) -> list[str]:
    pairs = []
    i = 0
    while i < len(text):
        pair = text[i:i+2]
        if len(pair) == 2 and pair[0] == pair[1]:
            pairs.append(pair[0] + 'x')
            i += 1
        else:
            if len(pair) == 1:
                pair += 'z'
            pairs.append(pair)
            i += 2
    return pairs

def generate_key_table(key: str) -> list[list[str]]:
    key = to_lowercase(key).replace('j', 'i')
    seen = []
    for c in key:
        if c not in seen and c in string.ascii_lowercase:
            seen.append(c)
    for c in string.ascii_lowercase.replace('j', ''):
        if c not in seen:
            seen.append(c)
    
    return [seen[i:i+5] for i in range(0, 25, 5)]

def search(matrix: list[list[str]], ch: str) -> tuple[int,int]:
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == ch:
                return r, c
    raise ValueError(f"Character {ch!r} not in key table")

def encrypt_pair(matrix, a: str, b: str) -> str:
    r1, c1 = search(matrix, a)
    r2, c2 = search(matrix, b)
    
    if r1 == r2:
        return matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5]
    
    if c1 == c2:
        return matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2]
    
    return matrix[r1][c2] + matrix[r2][c1]

def decrypt_pair(matrix, a: str, b: str) -> str:
    r1, c1 = search(matrix, a)
    r2, c2 = search(matrix, b)
    
    if r1 == r2:
        return matrix[r1][(c1 - 1) % 5] + matrix[r2][(c2 - 1) % 5]
    
    if c1 == c2:
        return matrix[(r1 - 1) % 5][c1] + matrix[(r2 - 1) % 5][c2]
    
    return matrix[r1][c2] + matrix[r2][c1]

def preprocess(text: str) -> list[str]:
    
    t = to_lowercase(text)
    t = remove_spaces(t).replace('j', 'i')
    
    return digraphs(t)

def encrypt(text: str, key: str) -> str:
    mat = generate_key_table(key)
    pairs = preprocess(text)
    return ''.join(encrypt_pair(mat, p[0], p[1]) for p in pairs)

def decrypt(text: str, key: str) -> str:
    mat = generate_key_table(key)
    
    pairs = [text[i:i+2] for i in range(0, len(text), 2)]
    return ''.join(decrypt_pair(mat, p[0], p[1]) for p in pairs)
