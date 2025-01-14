from src.downloader.http_handler import fetch_book
from src.aws.s3_manager import S3Manager

class Controller:
    def __init__(self, bucket_datalake_name):
        """
        Inicializa el controlador para gestionar libros.
        
        :param bucket_datalake_name: Nombre del bucket donde se almacenarán los libros descargados.
        """
        self.bucket_datalake_name = bucket_datalake_name
        self.s3_manager = S3Manager(region_name='us-east-1')

    def process_book(self, book_id):
        """
        Descarga y guarda un libro basado en el ID.
        
        :param book_id: ID del libro a descargar.
        """
        try:
            # Descargar el libro
            print(f"Descargando el libro con ID {book_id}...")
            book_content = fetch_book(book_id)

            s3_key = str(book_id) + ".txt"

            # Guardar el libro en S3
            self.s3_manager.upload_text_file(self.bucket_datalake_name, s3_key, book_content)
        except Exception as e:
            print(f"Error al procesar el libro {book_id}: {e}")

    def run_with_book_ids(self, book_ids):
        """
        Procesa una lista de libros basada en sus IDs.
        
        :param book_ids: Lista de IDs de libros a procesar.
        """
        for book_id in book_ids:
            self.process_book(book_id)
