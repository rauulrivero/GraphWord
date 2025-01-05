import re

class WordFilter:
    def __init__(self, dictionary, min_len=3, max_len=3):
        """
        Inicializa el filtrador de palabras.

        :param dictionary: Diccionario de palabras a filtrar.
        :param min_len: Longitud mínima de las palabras.
        :param max_len: Longitud máxima de las palabras.
        """
        self.dictionary = dictionary
        self.min_len = min_len
        self.max_len = max_len

    def filter_words(self):
        """
        Filtra las palabras del diccionario basándose en longitud y pronunciabilidad.

        :return: Diccionario filtrado.
        """
        return {
            word: value
            for word, value in self.dictionary.items()
            if self._is_valid_word(word)
        }

    def _is_valid_word(self, word):
        """
        Verifica si una palabra es válida según las reglas establecidas.

        :param word: La palabra a verificar.
        :return: True si la palabra es válida, False en caso contrario.
        """
        # Convertir la palabra a minúsculas
        word = word.lower()

        # Verificar si la palabra contiene solo caracteres alfabéticos
        if not word.isalpha():
            return False

        # Verificar la longitud de la palabra
        if not (self.min_len <= len(word) <= self.max_len):
            return False

        # Verificar si la palabra es pronunciable
        if not self._is_pronounceable(word):
            return False

        return True

    def _is_pronounceable(self, palabra):
        """
        Verifica si una palabra es pronunciable.

        :param palabra: La palabra a verificar.
        :return: True si la palabra es pronunciable, False en caso contrario.
        """
        # Rechazar secuencias repetitivas de consonantes o vocales
        if re.search(r'(.)\1{1,}', palabra): 
            return False
        
        # Eliminar palabras con secuencias no pronunciables (consonantes seguidas sin vocal)
        if re.search(r'[bcdfghjklmnpqrstvwxyz]{3,}', palabra): 
            return False

        # Eliminar palabras con secuencias de vocales no naturales
        if re.search(r'[aeiou]{3,}', palabra): 
            return False

        return True
