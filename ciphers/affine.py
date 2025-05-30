def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    if gcd(a, m) != 1:
        return None
    
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
    if isinstance(key, str):
        
        a, b = map(int, key.split(','))
    else:
        a, b = key
    
    
    if gcd(a, 26) != 1:
        raise ValueError("The 'a' value must be coprime with 26")
    
    result = ""
    for char in text:
        if char.isalpha():
            
            if char.isupper():
                x = ord(char) - ord('A')
                
                encrypted = (a * x + b) % 26
                result += chr(encrypted + ord('A'))
            else:
                x = ord(char) - ord('a')
                
                encrypted = (a * x + b) % 26
                result += chr(encrypted + ord('a'))
        else:
            result += char
    return result

def decrypt(text, key):
    if isinstance(key, str):
        
        a, b = map(int, key.split(','))
    else:
        a, b = key
    
    
    if gcd(a, 26) != 1:
        raise ValueError("The 'a' value must be coprime with 26")
    
    
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        raise ValueError("Cannot find multiplicative inverse")
    
    result = ""
    for char in text:
        if char.isalpha():
            
            if char.isupper():
                y = ord(char) - ord('A')
                
                decrypted = (a_inv * (y - b)) % 26
                result += chr(decrypted + ord('A'))
            else:
                y = ord(char) - ord('a')
                
                decrypted = (a_inv * (y - b)) % 26
                result += chr(decrypted + ord('a'))
        else:
            result += char
    return result