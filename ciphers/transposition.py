def encrypt(text, key):
    """
    Encrypt text using columnar transposition cipher
    key: number of columns
    """
    # Remove spaces for cleaner encryption (optional)
    clean_text = ''.join(text.split())
    
    # If text is empty after cleaning
    if not clean_text:
        return text
    
    columns = int(key)
    
    # Calculate number of rows needed
    rows = len(clean_text) // columns
    if len(clean_text) % columns != 0:
        rows += 1
    
    # Create grid
    grid = []
    for i in range(rows):
        row = []
        for j in range(columns):
            index = i * columns + j
            if index < len(clean_text):
                row.append(clean_text[index])
            else:
                row.append('')  # Padding
        grid.append(row)
    
    # Read column by column
    result = ""
    for col in range(columns):
        for row in range(rows):
            if grid[row][col]:  # Skip empty cells
                result += grid[row][col]
    
    return result

def decrypt(text, key):
    """
    Decrypt text using columnar transposition cipher
    key: number of columns
    """
    if not text:
        return text
    
    columns = int(key)
    rows = len(text) // columns
    if len(text) % columns != 0:
        rows += 1
    
    # Calculate how many columns will have extra characters
    extra_chars = len(text) % columns
    
    # Create grid
    grid = [['' for _ in range(columns)] for _ in range(rows)]
    
    # Fill grid column by column
    index = 0
    for col in range(columns):
        # Determine how many characters this column should have
        if col < extra_chars:
            chars_in_col = rows
        else:
            chars_in_col = rows - 1 if extra_chars > 0 else rows
        
        for row in range(chars_in_col):
            if index < len(text):
                grid[row][col] = text[index]
                index += 1
    
    # Read row by row
    result = ""
    for row in range(rows):
        for col in range(columns):
            if grid[row][col]:
                result += grid[row][col]
    
    return result