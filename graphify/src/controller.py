from src.utils.file_manager import FileManager
from src.utils.text_processor import TextProcessor
from src.utils.word_filter import WordFilter
from src.database.word_graph import WordGraph
from src.bookmanager.file_content_manager import FileContentManager
from src.aws.s3_manager import S3Manager

class Controller:
    def __init__(self, datalake_bucket, graph_bucket, s3_keys, s3_bucket_path,  min_len=3, max_len=3, region_name='us-east-1',):
        self.file_manager = FileManager()
        self.s3_manager = S3Manager(region_name=region_name)
        self.datalake_bucket = datalake_bucket
        self.graph_bucket = graph_bucket
        self.global_word_frequency_dict = {}
        self.s3_bucket_path = s3_bucket_path
        self.s3_keys = s3_keys
        self.min_len = min_len
        self.max_len = max_len

    def run(self):
        print("Starting the process to download and process books.")
        dict_books_text = self.s3_manager.download_txt_files_to_memory(self.datalake_bucket, self.s3_keys)
        print(f"Downloaded {len(dict_books_text)} books from S3.")

        for book_id, book_text in dict_books_text.items():
            print(f"Processing book ID: {book_id}")
            self._load_and_process_book(book_text)
            
        print("Creating the word graph.")
        word_graph = WordGraph(self.global_word_frequency_dict)
        json_data = word_graph.to_json()

        print("Uploading the word graph to S3.")
        self.s3_manager.upload_json_file(self.graph_bucket, json_data, self.s3_bucket_path)
        print("Graph successfully saved to S3.")

    def _load_and_process_book(self, book_text):

        content_manager = FileContentManager(book_text)
        content_part = content_manager.get_content_part()
        
        text_processor = TextProcessor(content_part)
        word_frequency_dict = text_processor.get_word_frequency()
        
        word_filter = WordFilter(word_frequency_dict, self.min_len, self.max_len)
        filtered_frecuency_dict = word_filter.filter_words()
        
        self._update_global_word_frequency(filtered_frecuency_dict)
        print("Book processing completed.")

    def _update_global_word_frequency(self, word_frequency_dict):
        print("Merging current book's word frequencies into the global dictionary.")
        for word, frequency in word_frequency_dict.items():
            if word in self.global_word_frequency_dict:
                self.global_word_frequency_dict[word] += frequency
            else:
                self.global_word_frequency_dict[word] = frequency
        print("Global dictionary updated.")
