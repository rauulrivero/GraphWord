from flask import Flask
<<<<<<< HEAD
from config.config import Config, ProductionConfig, DevelopmentConfig, TestingConfig
=======
from api.config.config import Config, ProductionConfig, DevelopmentConfig, TestingConfig
from api.src.utils.file_manager import FileManager
from database.graph import WordGraph
from src.aws.s3_manager import S3Manager
>>>>>>> 0839766c38b3ad09a484e7cff885d877dbf9bb15
from dotenv import load_dotenv


def create_app(config_class=Config):
    app = Flask(__name__)

    # Load environment variables
    load_dotenv()

    # Flask environment configuration
    if Config.FLASK_ENV == 'development':
        app.config.from_object(DevelopmentConfig)
    elif Config.FLASK_ENV == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(TestingConfig)  # Configuration for testing

    return app
