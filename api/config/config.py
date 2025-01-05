import os
from dotenv import load_dotenv

load_dotenv() 

class Config:
    FLASK_ENV = os.getenv('FLASK_ENV')
    FILE_PATH = os.getenv('FILE_PATH')

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True