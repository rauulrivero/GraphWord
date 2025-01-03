import requests

def fetch_book(book_id):
    try:
        # Realizar la solicitud para obtener el texto del libro
        response = requests.get(f'https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt')
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        raise Exception(f"Error al descargar el libro {book_id}: {e}")
