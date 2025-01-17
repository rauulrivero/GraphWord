from crawler.src.aws.s3_manager import S3Manager
from crawler.src.downloader.http_handler import fetch_book
import requests

def test_fetch_book():
    """
    Prueba la función fetch_book para descargar un libro.
    """
    test_book_id = 1342  # Ejemplo: Pride and Prejudice
    try:
        content = fetch_book(test_book_id)
        assert content.startswith("The Project Gutenberg EBook"), "El contenido del libro no es válido."
        print(f"[PASSED] fetch_book con book_id={test_book_id}")
    except Exception as e:
        print(f"[FAILED] fetch_book con book_id={test_book_id}: {e}")

def test_s3_upload():
    """
    Prueba la carga de un archivo de texto a S3.
    """
    bucket_name = "test-datalake"
    s3_key = "test_book.txt"
    content = "Este es un contenido de prueba."

    s3_manager = S3Manager(region_name="us-east-1")

    try:
        s3_manager.upload_text_file(bucket_name, s3_key, content)
        print(f"[PASSED] upload_text_file para {s3_key}")
    except Exception as e:
        print(f"[FAILED] upload_text_file para {s3_key}: {e}")


# def test_lambda_handler():
#     """
#     Prueba la función lambda_handler simulando un evento.
#     """
#     from lambda_function import lambda_handler

#     event = {
#         "book_ids": [1342, 11, 84]
#     }

#     context = {}  # Simulación de contexto

#     try:
#         response = lambda_handler(event, context)
#         assert response['statusCode'] == 200, "El estado HTTP no es 200."
#         print(f"[PASSED] lambda_handler con event={event}")
#     except Exception as e:
#         print(f"[FAILED] lambda_handler con event={event}: {e}")

if __name__ == "__main__":
    print("Iniciando pruebas del crawler...")

    # Probar cada componente individualmente
    test_fetch_book()
    test_s3_upload()
    # test_lambda_handler()

    print("Pruebas completadas.")
