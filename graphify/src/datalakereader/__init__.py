import os
from src.datalakereader.file_reader import read_text_file
from src.datalakereader.file_tokenizer import file_tokenizer
from src.utils.word_filter import filter_words

def process_datalake(datalake_path, min_len=3, max_len=5):
    """
    Procesa todos los archivos del datalake y combina las frecuencias de palabras.

    Args:
        datalake_path (str): Ruta al directorio del datalake.
        min_len (int): Longitud mínima de las palabras.
        max_len (int): Longitud máxima de las palabras.

    Returns:
        dict: Diccionario combinado de palabras y frecuencias.
    """
    combined_word_frequencies = {}

    # Iterar sobre todos los archivos en el directorio datalake
    for filename in os.listdir(datalake_path):
        file_path = os.path.join(datalake_path, filename)

        if os.path.isfile(file_path):  # Asegurarse de que sea un archivo
            content = read_text_file(file_path)

            # Tokenizar contenido y obtener el diccionario de palabras con frecuencias
            word_frequencies = file_tokenizer(content)
            print(f"Procesando archivo {filename} con {len(word_frequencies)} palabras...")

            # Filtrar palabras en función de sus características
            filtered_frequencies = filter_words(word_frequencies, min_len, max_len)
            print(f"Palabras filtradas: {len(filtered_frequencies)}")

            # Combinar frecuencias con el diccionario acumulado
            for word, freq in filtered_frequencies.items():
                combined_word_frequencies[word] = combined_word_frequencies.get(word, 0) + freq

    return combined_word_frequencies
