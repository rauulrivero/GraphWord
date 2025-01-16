import pytest
from unittest.mock import patch, MagicMock
from crawler.src.controller import Controller
from crawler.src.aws.s3_manager import S3Manager
# from crawler.src.downloader.http_handler import fetbch_book

class TestCrawler(unittest.TestCase):

    # @patch('src.downloader.http_handler.requests.get')
    # def test_fetch_book_success(self, mock_get):
    #     """Test para verificar que fetch_book descarga correctamente un libro."""
    #     mock_response = MagicMock()
    #     mock_response.status_code = 200
    #     mock_response.text = 'Contenido del libro de prueba'
    #     mock_get.return_value = mock_response

    #     book_id = 1234
    #     result = fetch_book(book_id)

    #     mock_get.assert_called_once_with(f'https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt')
    #     self.assertEqual(result, 'Contenido del libro de prueba')

    # @patch('src.downloader.http_handler.requests.get')
    # def test_fetch_book_failure(self, mock_get):
    #     """Test para verificar que fetch_book maneja errores correctamente."""
    #     mock_get.side_effect = Exception("Error al realizar la solicitud")

    #     book_id = 5678
    #     with self.assertRaises(Exception) as context:
    #         fetch_book(book_id)

    #     self.assertIn("Error al descargar el libro", str(context.exception))

    # @patch('src.aws.s3_manager.S3Manager.upload_text_file')
    # @patch('src.downloader.http_handler.fetch_book')
    # def test_process_book_success(self, mock_fetch_book, mock_upload_text_file):
    #     """Test para verificar que el método process_book funciona correctamente."""
    #     controller = Controller(bucket_datalake_name='test-bucket')

    #     book_id = 1234
    #     book_content = 'Contenido del libro de prueba'

    #     mock_fetch_book.return_value = book_content

    #     controller.process_book(book_id)

    #     mock_fetch_book.assert_called_once_with(book_id)
    #     mock_upload_text_file.assert_called_once_with('test-bucket', f'{book_id}.txt', book_content)

    @patch('src.controller.Controller.process_book')
    def test_run(self, mock_process_book):
        """Test para verificar que el método run procesa todos los libros de la lista."""
        controller = Controller(bucket_datalake_name='test-bucket')

        book_ids = [1234, 5678, 91011]

        controller.run(book_ids)

        self.assertEqual(mock_process_book.call_count, len(book_ids))
        for book_id in book_ids:
            mock_process_book.assert_any_call(book_id)

if __name__ == '__main__':
    unittest.main()
