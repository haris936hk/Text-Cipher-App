def encrypt(text, key):
    """
    Encrypt text using rail fence cipher
    key: number of rails
    """
    if not text:
        return text
    
    rails = int(key)
    if rails <= 1:
        return text
    
    # Create rails
    fence = [['' for _ in range(len(text))] for _ in range(rails)]
    
    # Direction: True for down, False for up
    direction = True
    rail = 0
    
    # Place characters in zigzag pattern
    for i, char in enumerate(text):
        fence[rail][i] = char
        
        # Change direction at top and bottom rails
        if rail == 0:
            direction = True
        elif rail == rails - 1:
            direction = False
        
        # Move to next rail
        if direction:
            rail += 1
        else:
            rail -= 1
    
    # Read rails to create cipher text
    result = ""
    for r in range(rails):
        for c in range(len(text)):
            if fence[r][c]:
                result += fence[r][c]
    
    return result

def decrypt(text, key):
    """
    Decrypt text using rail fence cipher
    key: number of rails
    """
    if not text:
        return text
    
    rails = int(key)
    if rails <= 1:
        return text
    
    # Create rails
    fence = [['' for _ in range(len(text))] for _ in range(rails)]
    
    # Mark positions in zigzag pattern
    direction = True
    rail = 0
    
    for i in range(len(text)):
        fence[rail][i] = '*'  # Mark position
        
        # Change direction at top and bottom rails
        if rail == 0:
            direction = True
        elif rail == rails - 1:
            direction = False
        
        # Move to next rail
        if direction:
            rail += 1
        else:
            rail -= 1
    
    # Fill the fence with cipher text
    index = 0
    for r in range(rails):
        for c in range(len(text)):
            if fence[r][c] == '*' and index < len(text):
                fence[r][c] = text[index]
                index += 1
    
    # Read in zigzag pattern to get original text
    result = ""
    direction = True
    rail = 0
    
    for i in range(len(text)):
        result += fence[rail][i]
        
        # Change direction at top and bottom rails
        if rail == 0:
            direction = True
        elif rail == rails - 1:
            direction = False
        
        # Move to next rail
        if direction:
            rail += 1
        else:
            rail -= 1
    
    return result