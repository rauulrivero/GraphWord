# Simplified Graphify Test
from graphify.src.utils.text_processor import TextProcessor

def test_text_processor():
    processor = TextProcessor("hello world hello")
    word_freq = processor.get_word_frequency()
    assert word_freq == {"hello": 2, "world": 1}