from crawler.src.aws.s3_manager import S3Manager
from crawler.src.downloader.http_handler import fetch_book
import requests

def test_fetch_book():
    test_book_id = 1342
    try:
        content = fetch_book(test_book_id)
        assert content.startswith("The Project Gutenberg EBook"), "The content of the book is invalid."
        print(f"[PASSED] fetch_book with book_id={test_book_id}")
    except Exception as e:
        print(f"[FAILED] fetch_book con book_id={test_book_id}: {e}")

def test_s3_upload():
    bucket_name = "test-datalake"
    s3_key = "test_book.txt"
    content = "This is test content."
    
    s3_manager = S3Manager(region_name="us-east-1")

    try:
        s3_manager.upload_text_file(bucket_name, s3_key, content)
        print(f"[PASSED] upload_text_file para {s3_key}")
    except Exception as e:
        print(f"[FAILED] upload_text_file para {s3_key}: {e}")


if __name__ == "__main__":

    test_fetch_book()
    test_s3_upload()
