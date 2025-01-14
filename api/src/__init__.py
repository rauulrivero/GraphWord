from flask import Flask
from config.config import Config, ProductionConfig, DevelopmentConfig, TestingConfig
from src.utils.file_manager import FileManager
from src.database.graph import WordGraph
from src.aws.s3_manager import S3Manager


def create_app(config_class=Config):
    app = Flask(__name__)

    bucket_name = 'books-graph2'
    json_file_key = 'graph.json'

    file_manager = FileManager()
    json_graph = None

    try:
        # Initialize AWSManager and download the JSON file
        aws_manager = S3Manager()
        temp_file_path = 'temp_graph.json'
        aws_manager.download_file(bucket_name, json_file_key, temp_file_path)

        # Read the JSON file using FileManager
        json_graph = file_manager.read_json(temp_file_path)

    except Exception as e:
        print(f"An error occurred while downloading or reading the S3 file: {e}")

    # Initialize the graph
    if json_graph is not None:
        word_graph = WordGraph(json_graph)
    else:
        word_graph = WordGraph()

    app.graph = word_graph.get_graph()

    # Flask environment configuration
    if Config.FLASK_ENV == 'development':
        app.config.from_object(DevelopmentConfig)
    elif Config.FLASK_ENV == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(TestingConfig)  # Configuration for testing

    return app
