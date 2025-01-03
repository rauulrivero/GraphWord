from downloader.http_handler import fetch_book
from utils.file_manager import FileManager

class Controller:
    def __init__(self, datalake_path):
        """
        Inicializa el controlador para gestionar libros.
        
        :param datalake_path: Ruta base donde se almacenarán los libros descargados.
        """
        self.datalake_path = datalake_path
        self.file_manager = FileManager()

    def process_books(self, book_id):
        """
        Descarga y guarda un libro basado en el ID.
        
        :param book_id: ID del libro a descargar.
        """
        try:
            # Descargar el libro
            print(f"Descargando el libro con ID {book_id}...")
            book_content = fetch_book(book_id)
            
            # Ruta completa para guardar el libro
            file_path = f"{self.datalake_path}/{book_id}.txt"
            
            # Guardar el contenido del libro
            self.file_manager.save_text_to_file(book_content, file_path)
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
