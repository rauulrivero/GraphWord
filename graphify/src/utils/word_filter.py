import re

def filter_words(dictionary, min_len=3, max_len=3):
    """
    Filtra un diccionario manteniendo solo palabras pronunciables 
    y con longitud entre min_len y max_len.

    Args:
        dictionary (dict): Diccionario donde las claves son palabras.
        min_len (int): Longitud mínima de las palabras.
        max_len (int): Longitud máxima de las palabras.

    Returns:
        dict: Diccionario filtrado.
    """
    return {
        word: value
        for word, value in dictionary.items()
        if is_valid_word(word, min_len, max_len)
    }


def is_valid_word(word, min_len=3, max_len=3):
    # Función para filtrar palabras no pronunciables y con caracteres inválidos

    # Convertir a minúsculas para evitar duplicados por mayúsculas
    word = word.lower()

    # Verificar si la palabra contiene solo caracteres alfabéticos
    if not word.isalpha(): return False

    # Verificar la longitud de la palabra
    if not (min_len <= len(word) <= max_len): return False

    # Verificar si la palabra es pronunciable
    if not is_pronounceable(word): return False

    return True


def is_pronounceable(palabra):
    # Función para verificar si una palabra es pronunciable
    
    # Rechazar secuencias repetitivas de consonantes o vocales (dos o más repeticiones)
    # Detectar caracteres repetidos 2 veces o más
    if re.search(r'(.)\1{1,}', palabra): return False
    
    # Eliminar palabras con secuencias no pronunciables (consonantes seguidas sin vocal)
    # 3 o más consonantes seguidas
    if re.search(r'[bcdfghjklmnpqrstvwxyz]{3,}', palabra): return False

    # Eliminar palabras con secuencias de vocales no naturales
    # 3 o más vocales seguidas
    if re.search(r'[aeiou]{3,}', palabra): return False

    return True
