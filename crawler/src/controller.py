from src.downloader.http_handler import fetch_book
from src.aws.s3_manager import S3Manager

class Controller:
    def __init__(self, bucket_datalake_name):
        """
        Initializes the controller for managing books.
        
        :param bucket_datalake_name: Name of the bucket where downloaded books will be stored.
        """
        self.bucket_datalake_name = bucket_datalake_name
        self.s3_manager = S3Manager(region_name='us-east-1')

    def process_book(self, book_id):
        """
        Downloads and saves a book based on its ID.
        
        :param book_id: ID of the book to download.
        """
        try:
            print(f"Downloading the book with ID {book_id}...")
            book_content = fetch_book(book_id)

            s3_key = str(book_id) + ".txt"

            self.s3_manager.upload_text_file(self.bucket_datalake_name, s3_key, book_content)
        except Exception as e:
            print(f"Error processing book {book_id}: {e}")

    def run(self, book_ids):
        """
        Processes a list of books based on their IDs.
        
        :param book_ids: List of book IDs to process.
        """
        for book_id in book_ids:
            self.process_book(book_id)
