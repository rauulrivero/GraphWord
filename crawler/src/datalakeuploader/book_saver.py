from downloader.http_handler import fetch_book
from utils.utils import extract_book_content

def save_book_content(book_id):
    try:
        # Obtener el contenido bruto del libro desde la web
        text = fetch_book(book_id)
        
        # Extraer el contenido relevante del libro
        content = extract_book_content(text)

        
        if content:
            # Guardar el contenido en un archivo local
            with open(f'C:/Users/rauul/Desktop/GCID 4º/TCSD/proyecto/datalake/{book_id}.txt', 'w') as file:
                file.write(content)
                print(f"Libro {book_id} guardado correctamente.")
        else:
            print(f"El libro {book_id} no contiene el formato esperado.")
    except Exception as e:
        print(f"Error al procesar el libro {book_id}: {e}")
