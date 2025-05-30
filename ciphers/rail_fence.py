def encrypt(text, key):
    if not text:
        return text
    
    rails = int(key)
    if rails <= 1:
        return text
    
    
    fence = [['' for _ in range(len(text))] for _ in range(rails)]
    
    
    direction = True
    rail = 0
    
    
    for i, char in enumerate(text):
        fence[rail][i] = char
        
        
        if rail == 0:
            direction = True
        elif rail == rails - 1:
            direction = False
        
        
        if direction:
            rail += 1
        else:
            rail -= 1
    
    
    result = ""
    for r in range(rails):
        for c in range(len(text)):
            if fence[r][c]:
                result += fence[r][c]
    
    return result

def decrypt(text, key):
    if not text:
        return text
    
    rails = int(key)
    if rails <= 1:
        return text
    
    
    fence = [['' for _ in range(len(text))] for _ in range(rails)]
    
    
    direction = True
    rail = 0
    
    for i in range(len(text)):
        fence[rail][i] = '*'  
        
        
        if rail == 0:
            direction = True
        elif rail == rails - 1:
            direction = False
        
        
        if direction:
            rail += 1
        else:
            rail -= 1
    
    
    index = 0
    for r in range(rails):
        for c in range(len(text)):
            if fence[r][c] == '*' and index < len(text):
                fence[r][c] = text[index]
                index += 1
    
    
    result = ""
    direction = True
    rail = 0
    
    for i in range(len(text)):
        result += fence[rail][i]
        
        
        if rail == 0:
            direction = True
        elif rail == rails - 1:
            direction = False
        
        
        if direction:
            rail += 1
        else:
            rail -= 1
    
    return result