import string

def to_lowercase(text: str) -> str:
    return text.lower()

def remove_spaces(text: str) -> str:
    return ''.join(c for c in text if c != ' ')

def digraphs(text: str) -> list[str]:
    """Split text into digraphs (pairs), padding the last if needed."""
    pairs = []
    i = 0
    while i < len(text):
        pair = text[i:i+2]
        if len(pair) == 2 and pair[0] == pair[1]:
            # insert filler and re-process the same second character
            pairs.append(pair[0] + 'x')
            i += 1
        else:
            if len(pair) == 1:
                pair += 'z'
            pairs.append(pair)
            i += 2
    return pairs

def generate_key_table(key: str) -> list[list[str]]:
    """Create 5×5 matrix from key + alphabet (dropping 'j')."""
    key = to_lowercase(key).replace('j', 'i')
    seen = []
    for c in key:
        if c not in seen and c in string.ascii_lowercase:
            seen.append(c)
    for c in string.ascii_lowercase.replace('j', ''):
        if c not in seen:
            seen.append(c)
    # Build matrix rows of 5 letters each
    return [seen[i:i+5] for i in range(0, 25, 5)]

def search(matrix: list[list[str]], ch: str) -> tuple[int,int]:
    """Find (row, col) of letter in matrix."""
    for r in range(5):
        for c in range(5):
            if matrix[r][c] == ch:
                return r, c
    raise ValueError(f"Character {ch!r} not in key table")

def encrypt_pair(matrix, a: str, b: str) -> str:
    r1, c1 = search(matrix, a)
    r2, c2 = search(matrix, b)
    # same row
    if r1 == r2:
        return matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5]
    # same column
    if c1 == c2:
        return matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2]
    # rectangle swap
    return matrix[r1][c2] + matrix[r2][c1]

def decrypt_pair(matrix, a: str, b: str) -> str:
    r1, c1 = search(matrix, a)
    r2, c2 = search(matrix, b)
    # same row
    if r1 == r2:
        return matrix[r1][(c1 - 1) % 5] + matrix[r2][(c2 - 1) % 5]
    # same column
    if c1 == c2:
        return matrix[(r1 - 1) % 5][c1] + matrix[(r2 - 1) % 5][c2]
    # rectangle swap
    return matrix[r1][c2] + matrix[r2][c1]

def preprocess(text: str) -> list[str]:
    # 1) lowercase, remove spaces, replace j→i
    t = to_lowercase(text)
    t = remove_spaces(t).replace('j', 'i')
    # 2) create digraphs with filler logic
    return digraphs(t)

def encrypt(text: str, key: str) -> str:
    mat = generate_key_table(key)
    pairs = preprocess(text)
    return ''.join(encrypt_pair(mat, p[0], p[1]) for p in pairs)

def decrypt(text: str, key: str) -> str:
    mat = generate_key_table(key)
    # assume ciphertext already has even length of letters
    pairs = [text[i:i+2] for i in range(0, len(text), 2)]
    return ''.join(decrypt_pair(mat, p[0], p[1]) for p in pairs)
