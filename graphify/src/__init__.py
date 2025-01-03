from flask import Flask
from config.config import Config, ProductionConfig, DevelopmentConfig, TestingConfig
from src.database.graph import generate_graph
from src.datalakereader import process_datalake

MIN_LENGTH = 3
MAX_LENGTH = 5


def create_app(config_class=Config):
    app = Flask(__name__)

    # Ruta al directorio del datalake
    datalake_path = "C:/Users/rauul/Desktop/GCID 4º/TCSD/proyecto/datalake"
    
    # Procesar el datalake y combinar las frecuencias de palabras
    print("Procesando el datalake...")
    combined_word_frequencies = process_datalake(datalake_path, MIN_LENGTH, MAX_LENGTH)

    # Generar el grafo con las palabras filtradas y sus frecuencias acumuladas
    print("Generando grafo con todas las palabras filtradas y sus frecuencias acumuladas...")
    app.graph = generate_graph(combined_word_frequencies)

    # Configuración del entorno de Flask
    if Config.FLASK_ENV == 'development':
        app.config.from_object(DevelopmentConfig)
    elif Config.FLASK_ENV == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(TestingConfig)  # Configuración para testing

    return app
