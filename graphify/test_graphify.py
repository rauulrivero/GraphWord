from graphify.src.utils.file_manager import FileManager
from graphify.src.utils.text_processor import TextProcessor
from graphify.src.utils.word_filter import WordFilter
from graphify.src.database.word_graph import WordGraph
from graphify.src.aws.s3_manager import S3Manager
import pytest



def test_file_manager():
    """
    Test FileManager functions such as reading, saving, and loading JSON files.
    """
    file_manager = FileManager()
    test_text = "word1 word2 word3 word1"
    test_path = "test_graph.json"

    try:
        graph = WordGraph({"word1": 2, "word2": 1, "word3": 1}).get_graph()
        file_manager.save_graph_to_json(graph, test_path)

        loaded_graph = file_manager.load_graph_from_json(test_path)
        assert graph.number_of_nodes() == loaded_graph.number_of_nodes(), "Nodes mismatch"
        assert graph.number_of_edges() == loaded_graph.number_of_edges(), "Edges mismatch"
        print("[PASSED] FileManager tests")
    except Exception as e:
        print(f"[FAILED] FileManager tests: {e}")


def test_text_processor():
    """
    Test TextProcessor for correct tokenization and frequency calculation.
    """
    test_content = "word1 word2 word3 word1 word2"
    processor = TextProcessor(test_content)

    try:
        freq = processor.get_word_frequency()
        assert freq["word1"] == 2, "Frequency of word1 incorrect"
        assert freq["word2"] == 2, "Frequency of word2 incorrect"
        assert freq["word3"] == 1, "Frequency of word3 incorrect"
        print("[PASSED] TextProcessor tests")
    except Exception as e:
        print(f"[FAILED] TextProcessor tests: {e}")


def test_word_filter():
    """
    Test WordFilter for filtering based on length and validity.
    """
    test_dict = {"abc": 2, "abcd": 1, "a": 3, "123": 4, "aaaa": 1}
    filter_obj = WordFilter(test_dict, min_len=3, max_len=3)

    try:
        filtered = filter_obj.filter_words()
        assert "abc" in filtered, "Valid word abc not in filtered output"
        assert "abcd" not in filtered, "Invalid word abcd in filtered output"
        assert "a" not in filtered, "Invalid word a in filtered output"
        print("[PASSED] WordFilter tests")
    except Exception as e:
        print(f"[FAILED] WordFilter tests: {e}")


def test_word_graph():
    """
    Test WordGraph for graph generation and connectivity.
    """
    word_dict = {"cat": 3, "bat": 2, "rat": 1}
    graph = WordGraph(word_dict)

    try:
        g = graph.get_graph()
        assert g.number_of_nodes() == 3, "Graph nodes mismatch"
        assert g.number_of_edges() == 3, "Graph edges mismatch"
        assert "cat" in g, "Node cat not found in graph"
        assert g.has_edge("cat", "bat"), "Edge cat-bat not found"
        print("[PASSED] WordGraph tests")
    except Exception as e:
        print(f"[FAILED] WordGraph tests: {e}")


if __name__ == "__main__":

    test_file_manager()
    test_text_processor()
    test_word_filter()
    test_word_graph()
