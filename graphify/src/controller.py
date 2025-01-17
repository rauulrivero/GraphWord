from src.utils.file_manager import FileManager
from src.utils.text_processor import TextProcessor
from src.utils.word_filter import WordFilter
from src.database.word_graph import WordGraph
from src.bookmanager.file_content_manager import FileContentManager
from src.aws.s3_manager import S3Manager

class Controller:
    def __init__(self, datalake_bucket, graph_bucket, s3_keys, s3_bucket_path, region_name='us-east-1'):
        """
        Controlador general para gestionar la lectura de archivos, procesamiento de texto y generación de grafos de palabras 
        desde los ficheros de una carpeta.

        :param folder_path: Ruta a la carpeta que contiene los archivos a procesar.
        """
        self.file_manager = FileManager()
        self.s3_manager = S3Manager(region_name=region_name)
        
        self.datalake_bucket = datalake_bucket
        self.graph_bucket = graph_bucket
        self.global_word_frequency_dict = {}
        self.s3_bucket_path = s3_bucket_path
        self.s3_keys = s3_keys

    def run(self):
        """
        Controla el flujo de carga y procesamiento de todos los archivos en la carpeta especificada,
        generando y guardando los grafos en formato JSON.

        :return: Ningún valor, pero guarda los grafos como archivos JSON en la carpeta de salida.
        """
        # Descargar los archivos de la carpeta S3
        dict_books_text = self.s3_manager.download_txt_files_to_memory(self.datalake_bucket, self.s3_keys)
        
        for book_id, book_text in dict_books_text.items():
            print(f"Processing book ID: {book_id}")
            self._load_and_process_book(book_text)

        print("Diccionario de frecuencias global actualizado.")

        # Crear un grafo para las palabras globales
        word_graph = WordGraph(self.global_word_frequency_dict)

        # Guardar el grafo en S3
        json_data = word_graph.to_json()

        self.s3_manager.upload_json_file(self.graph_bucket, json_data, self.s3_bucket_path)

        print("Grafo guardado en S3.")

    def _load_and_process_book(self, book_text):
        """
        Controla el flujo de carga del archivo, procesamiento de texto y generación del grafo.

        :param file_path: Ruta al archivo de texto a procesar.
        :return: Grafo generado con las palabras filtradas.
        """

        # Paso 2: Procesar el contenido del libro
        content_manager = FileContentManager(book_text)
        content_part = content_manager.get_content_part()

        # Paso 3: Tokenizar el contenido
        text_processor = TextProcessor(content_part)
        word_frequency_dict = text_processor.get_word_frequency()

        # Paso 5: Filtrar las palabras según las reglas
        word_filter = WordFilter(word_frequency_dict)
        filtered_frecuency_dict = word_filter.filter_words()

        # Paso 4: Actualizar el diccionario global de frecuencias
        self._update_global_word_frequency(filtered_frecuency_dict)

        return None
    

    def _update_global_word_frequency(self, word_frequency_dict):
        """
        Actualiza el diccionario global de frecuencias con las frecuencias del archivo actual.

        :param word_frequency_dict: Diccionario de frecuencias de palabras para un archivo.
        """
        for word, frequency in word_frequency_dict.items():
            if word in self.global_word_frequency_dict:
                self.global_word_frequency_dict[word] += frequency
            else:
                self.global_word_frequency_dict[word] = frequency
        return None
