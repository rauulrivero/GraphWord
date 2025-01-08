from flask import Flask
from config.config import Config, ProductionConfig, DevelopmentConfig, TestingConfig
from src.utils.file_manager import FileManager
from src.database.graph import WordGraph
from src.aws.aws_manager import AWSManager
import os
import dotenv

def create_app(config_class=Config):
    app = Flask(__name__)


    dotenv.load_dotenv()
    aws_access_key = aws_access_key or os.getenv('aws_access_key_id')
    aws_secret_key = aws_secret_key or os.getenv('aws_secret_access_key')
    bucket_name = bucket_name or os.getenv('BUCKET_NAME')

    # S3 configuration
    json_file_key = 'graph.json'

    file_manager = FileManager()
    json_graph = None

    dotenv.load_dotenv()
    aws_access_key = aws_access_key or os.getenv('aws_access_key_id')
    aws_secret_key = aws_secret_key or os.getenv('aws_secret_access_key')

    try:
        # Initialize AWSManager and download the JSON file
        aws_manager = AWSManager(aws_access_key, aws_secret_key)
        temp_file_path = 'temp_graph.json'
        aws_manager.s3_client.download_file(bucket_name, json_file_key, temp_file_path)

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
