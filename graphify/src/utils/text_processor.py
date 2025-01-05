class TextProcessor:
    def __init__(self, content):
        """
        Inicializa el procesador de texto con el contenido a analizar.

        :param content: El contenido del texto como una cadena de caracteres.
        """
        self.content = content

    def tokenizer(self):
        """
        Tokeniza el contenido en palabras y calcula su frecuencia.

        :return: Un diccionario con palabras como claves y su frecuencia como valores.
        """
        words = self.content.split()
        word_freq = {}
        for word in words:
            word = word.strip().lower()  # Normalización de palabras: elimina espacios y convierte a minúsculas
            if word in word_freq:
                word_freq[word] += 1
            else:
                word_freq[word] = 1
        return word_freq

    def get_word_frequency(self):
        """
        Obtiene el diccionario de frecuencias de las palabras.

        :return: Diccionario con palabras y sus frecuencias.
        """
        return self.tokenizer()
