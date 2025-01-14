import sys
import os

# Imprime las rutas donde Python busca módulos
print("PYTHONPATH:", sys.path)

# Lista los archivos y directorios en la raíz del proyecto
print("Archivos en la raíz del proyecto:")
print(os.listdir(os.getcwd()))

# Lista los archivos y directorios en el directorio `api`
print("Archivos en el directorio 'api':")
print(os.listdir(os.path.join(os.getcwd(), "api")))

# Simplified API Test
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask
from api.src.routes.routes import api


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(api)
    app.testing = True
    return app.test_client()

@patch('src.services.graph_services.GraphServices.shortest_path')
def test_api_shortest_path(mock_shortest_path, client):
    mock_shortest_path.return_value = {'path': ['A', 'B'], 'length': 1}
    response = client.get('/shortest-path?origen=A&destino=B')
    assert response.status_code == 200
