import re

def extract_book_content(text):
    # Usar expresiones regulares para identificar el inicio y el final del contenido
    start_pattern = r"\*\*\* START OF THE PROJECT GUTENBERG EBOOK .* \*\*\*"
    end_pattern = r"\*\*\* END OF THE PROJECT GUTENBERG EBOOK .* \*\*\*"
    
    # Encontrar el índice de inicio y final del contenido del libro
    start_match = re.search(start_pattern, text)
    end_match = re.search(end_pattern, text)
    
    if start_match and end_match:
        # Extraer solo el contenido entre los patrones
        return text[start_match.end():end_match.start()].strip()
    
    return None
