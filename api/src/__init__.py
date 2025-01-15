from flask import Flask
from api.config.config import Config, ProductionConfig, DevelopmentConfig, TestingConfig
from api.src.utils.file_manager import FileManager
from database.graph import WordGraph
from src.aws.s3_manager import S3Manager
from dotenv import load_dotenv
import os


def create_app(config_class=Config):
    app = Flask(__name__)


    # Load environment variables
    load_dotenv()

    # Get the S3 bucket name and JSON file key
    bucket_name = os.getenv('S3_BUCKET_NAME')
    json_file_key = os.getenv('JSON_FILE_KEY')

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
