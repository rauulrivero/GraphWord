class FileContentManager:
    def __init__(self, book_text):
        """
        Inicializa el administrador de contenido del archivo.
        :param book_text: Texto completo del libro.
        """
        self.CONTENT_START_PATTERN = "*** START OF THE PROJECT GUTENBERG"
        self.METADATA_START_PATTERN = "Title:"
        self.CONTENT_END_PATTERN = "*** END OF THE PROJECT GUTENBERG"

        self.book_text = book_text

    def get_metadata_part(self):
        """
        Obtiene la parte de metadatos del texto del libro.
        :return: Substring con los metadatos.
        """
        return self.book_text[self.find_metadata_start_index():self.find_metadata_end_index()]

    def get_content_part(self):
        """
        Obtiene la parte de contenido del texto del libro.
        :return: Substring con el contenido del libro.
        """
        return self.book_text[self.find_content_start_index():self.find_content_end_index()]

    def find_content_start_index(self):
        """
        Encuentra el índice inicial del contenido del libro.
        :return: Índice inicial del contenido.
        """
        pattern_start = self.book_text.find(self.CONTENT_START_PATTERN)
        pattern_end = pattern_start + len(self.CONTENT_START_PATTERN)
        remaining_text = self.book_text[pattern_end:]
        return pattern_end + remaining_text.find("***") + 3

    def find_content_end_index(self):
        """
        Encuentra el índice final del contenido del libro.
        :return: Índice final del contenido.
        """
        return self.book_text.find(self.CONTENT_END_PATTERN)

    def find_metadata_end_index(self):
        """
        Encuentra el índice final de los metadatos.
        :return: Índice final de los metadatos.
        """
        return self.book_text.find(self.CONTENT_START_PATTERN)

    def find_metadata_start_index(self):
        """
        Encuentra el índice inicial de los metadatos.
        :return: Índice inicial de los metadatos.
        """
        return self.book_text.find(self.METADATA_START_PATTERN)
