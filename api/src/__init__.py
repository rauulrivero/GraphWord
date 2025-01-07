from flask import Flask
from config.config import Config, ProductionConfig, DevelopmentConfig, TestingConfig
from src.utils.file_manager import FileManager
from src.database.graph import WordGraph


def create_app(config_class=Config):
    app = Flask(__name__)

    json_path = 'graph.json'

    file_manager = FileManager()

    # Leer el json y incializar el grafo
    json_graph = file_manager.read_json(json_path)

    if json_graph is not None:
        word_graph = WordGraph(json_graph)
    else:
        word_graph = WordGraph()

    app.graph = word_graph.get_graph()


    # Configuracion del entorno de Flask
    if Config.FLASK_ENV == 'development':
        app.config.from_object(DevelopmentConfig)
    elif Config.FLASK_ENV == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(TestingConfig)  # Configuracion para testing

    return app
