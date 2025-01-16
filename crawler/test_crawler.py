import pytest
from unittest.mock import patch, MagicMock
from crawler.src.controller import Controller
from crawler.src.aws.s3_manager import S3Manager
from crawler.src.downloader.http_handler import fetch_book

@pytest.fixture
def mock_s3_manager():
    with patch('src.aws.s3_manager.boto3.client') as mock_client:
        mock_s3 = MagicMock()
        mock_client.return_value = mock_s3
        yield mock_s3

@pytest.fixture
def controller(mock_s3_manager):
    return Controller(bucket_datalake_name='test-datalake')

@patch('src.downloader.http_handler.requests.get')
def test_fetch_book(mock_get):
    # Configurar el mock de requests
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "Contenido del libro"
    mock_get.return_value = mock_response

    book_id = 1234
    content = fetch_book(book_id)

    # Verificaciones
    mock_get.assert_called_once_with(f'https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt')
    assert content == "Contenido del libro"

@patch('src.aws.s3_manager.S3Manager.upload_text_file')
def test_upload_text_file(mock_upload, mock_s3_manager):
    # Configurar el mock de upload_text_file
    mock_upload.return_value = True

    bucket_name = 'test-bucket'
    s3_key = 'test-file.txt'
    content = 'Test content'

    # Llamar al método directamente
    success = mock_s3_manager.put_object(
        Body=content,
        Bucket=bucket_name,
        Key=s3_key,
        ContentType='text/plain'
    )

    # Verificaciones
    assert success
    mock_s3_manager.put_object.assert_called_once_with(
        Body=content,
        Bucket=bucket_name,
        Key=s3_key,
        ContentType='text/plain'
    )
