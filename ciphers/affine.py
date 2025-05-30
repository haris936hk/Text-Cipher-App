def gcd(a, b):
    """Calculate Greatest Common Divisor"""
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    """Find modular multiplicative inverse of a modulo m"""
    if gcd(a, m) != 1:
        return None
    
    # Extended Euclidean Algorithm
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    _, x, _ = extended_gcd(a, m)
    return (x % m + m) % m

def encrypt(text, key):
    """
    Encrypt text using affine cipher
    key: tuple (a, b) where a and b are integers
    Formula: E(x) = (ax + b) mod 26
    """
    if isinstance(key, str):
        # Parse key from string format "a,b"
        a, b = map(int, key.split(','))
    else:
        a, b = key
    
    # Check if 'a' is coprime with 26
    if gcd(a, 26) != 1:
        raise ValueError("The 'a' value must be coprime with 26")
    
    result = ""
    for char in text:
        if char.isalpha():
            # Convert to number (A=0, B=1, ..., Z=25)
            if char.isupper():
                x = ord(char) - ord('A')
                # Apply affine transformation
                encrypted = (a * x + b) % 26
                result += chr(encrypted + ord('A'))
            else:
                x = ord(char) - ord('a')
                # Apply affine transformation
                encrypted = (a * x + b) % 26
                result += chr(encrypted + ord('a'))
        else:
            result += char
    return result

def decrypt(text, key):
    """
    Decrypt text using affine cipher
    key: tuple (a, b) where a and b are integers
    Formula: D(y) = a^(-1)(y - b) mod 26
    """
    if isinstance(key, str):
        # Parse key from string format "a,b"
        a, b = map(int, key.split(','))
    else:
        a, b = key
    
    # Check if 'a' is coprime with 26
    if gcd(a, 26) != 1:
        raise ValueError("The 'a' value must be coprime with 26")
    
    # Find multiplicative inverse of 'a' modulo 26
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        raise ValueError("Cannot find multiplicative inverse")
    
    result = ""
    for char in text:
        if char.isalpha():
            # Convert to number (A=0, B=1, ..., Z=25)
            if char.isupper():
                y = ord(char) - ord('A')
                # Apply inverse affine transformation
                decrypted = (a_inv * (y - b)) % 26
                result += chr(decrypted + ord('A'))
            else:
                y = ord(char) - ord('a')
                # Apply inverse affine transformation
                decrypted = (a_inv * (y - b)) % 26
                result += chr(decrypted + ord('a'))
        else:
            result += char
    return result