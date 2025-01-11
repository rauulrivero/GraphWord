from src.downloader.http_handler import fetch_book
from src.aws.s3_manager import S3Manager

class Controller:
    def __init__(self, bucket_datalake_name):
        """
        Inicializa el controlador para gestionar libros.
        
        :param datalake_path: Ruta base donde se almacenarán los libros descargados.
        """
        self.bucket_datalake_name = bucket_datalake_name
        self.s3_manager = S3Manager(region_name='us-east-1')

    def process_books(self, book_id):
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

    def run(self, start_id, n_books):
        """
        Procesa una serie de libros comenzando desde un ID específico.
        
        :param start_id: ID del primer libro a procesar.
        :param n_books: Número total de libros a procesar.
        """
        for i in range(start_id, start_id + n_books):
            self.process_books(i)
