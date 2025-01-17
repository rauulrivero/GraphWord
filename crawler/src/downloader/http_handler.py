import requests

def fetch_book(book_id):
    try:
        response = requests.get(f'https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt')
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        raise Exception(f"Error downloading book {book_id}: {e}")

