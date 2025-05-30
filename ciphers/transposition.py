def encrypt(text, key):
    clean_text = ''.join(text.split())
    
    
    if not clean_text:
        return text
    
    columns = int(key)
    
    
    rows = len(clean_text) // columns
    if len(clean_text) % columns != 0:
        rows += 1
    
    
    grid = []
    for i in range(rows):
        row = []
        for j in range(columns):
            index = i * columns + j
            if index < len(clean_text):
                row.append(clean_text[index])
            else:
                row.append('')  
        grid.append(row)
    
    
    result = ""
    for col in range(columns):
        for row in range(rows):
            if grid[row][col]:  
                result += grid[row][col]
    
    return result

def decrypt(text, key):
    if not text:
        return text
    
    columns = int(key)
    rows = len(text) // columns
    if len(text) % columns != 0:
        rows += 1
    
    
    extra_chars = len(text) % columns
    
    
    grid = [['' for _ in range(columns)] for _ in range(rows)]
    
    
    index = 0
    for col in range(columns):
        
        if col < extra_chars:
            chars_in_col = rows
        else:
            chars_in_col = rows - 1 if extra_chars > 0 else rows
        
        for row in range(chars_in_col):
            if index < len(text):
                grid[row][col] = text[index]
                index += 1
    
    
    result = ""
    for row in range(rows):
        for col in range(columns):
            if grid[row][col]:
                result += grid[row][col]
    
    return result