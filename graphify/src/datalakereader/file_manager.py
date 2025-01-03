class TextFileProcessor:
    def read_text_file(self, file_path):
        """
        Lee el contenido de un archivo de texto y lo devuelve como un string.
        :param file_path: Ruta al archivo.
        :return: Contenido del archivo como un string.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            return text
        except FileNotFoundError:
            print(f"El archivo {file_path} no se encontró.")
        except Exception as e:
            print(f"Ocurrió un error al leer el archivo: {e}")
            return None

    def file_tokenizer(self, content):
        """
        Tokeniza el contenido de un texto en palabras y calcula su frecuencia.
        :param content: Contenido del texto como un string.
        :return: Un diccionario con palabras como claves y su frecuencia como valores.
        """
        words = content.split()
        word_freq = {}
        for word in words:
            word = word.strip().lower()  # Normalizar: eliminar espacios y convertir a minúsculas
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1
        return word_freq
