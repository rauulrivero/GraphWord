from flask import Flask
from config.config import Config, ProductionConfig, DevelopmentConfig, TestingConfig
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
