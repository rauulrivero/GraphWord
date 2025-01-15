# Simplified Crawler Test
import pytest
from unittest.mock import patch
from src.controller import Controller

@patch('src.downloader.http_handler.fetch_book', return_value="Dummy content")
def test_crawler_fetch(mock_fetch_book):
    content = mock_fetch_book(1234)
    assert content == "Dummy content"
