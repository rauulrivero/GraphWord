import pytest
from unittest.mock import MagicMock, patch
from flask import Flask
from api.src import create_app
from api.src.routes.routes import api
from api.src.services.graph_services import GraphServices
import json

@pytest.fixture
def client():
    # Configura la aplicación Flask en modo de prueba
    app = create_app()
    app.register_blueprint(api)
    app.testing = True

    # Mock del grafo para pruebas
    mock_graph = MagicMock()
    app.graph = mock_graph

    return app.test_client()

@patch('src.services.graph_services.GraphServices.shortest_path')
def test_shortest_path(mock_shortest_path, client):
    # Configurar el mock
    mock_shortest_path.return_value = {
        'path': ['A', 'B', 'C'],
        'length': 2
    }

    # Llamar al endpoint
    response = client.get('/shortest-path?origen=A&destino=C')

    # Verificaciones
    assert response.status_code == 200
    data = response.get_json()
    assert data['path'] == ['A', 'B', 'C']
    assert data['length'] == 2

@patch('src.services.graph_services.GraphServices.isolated_nodes')
def test_isolated_nodes(mock_isolated_nodes, client):
    # Configurar el mock
    mock_isolated_nodes.return_value = {
        'isolated_nodes': ['X', 'Y', 'Z']
    }

    # Llamar al endpoint
    response = client.get('/isolated-nodes')

    # Verificaciones
    assert response.status_code == 200
    data = response.get_json()
    assert data['isolated_nodes'] == ['X', 'Y', 'Z']

@patch('src.services.graph_services.GraphServices.detect_clusters')
def test_detect_clusters(mock_detect_clusters, client):
    # Configurar el mock
    mock_detect_clusters.return_value = {
        'clusters': [['A', 'B'], ['C', 'D', 'E']]
    }

    # Llamar al endpoint
    response = client.get('/detect-clusters')

    # Verificaciones
    assert response.status_code == 200
    data = response.get_json()
    assert data['clusters'] == [['A', 'B'], ['C', 'D', 'E']]

# @patch('src.services.graph_services.GraphServices.nodes_with_highest_degree')
# def test_nodes_with_highest_degree(mock_nodes_with_highest_degree, client):
#     # Configurar el mock
#     mock_nodes_with_highest_degree.return_value = {
#         'nodes_with_highest_degree': [('A', 5), ('B', 4), ('C', 4)]
#     }

#     # Llamar al endpoint
#     response = client.get('/nodes-with-highest-degree')

#     # Verificaciones
#     assert response.status_code == 200
#     data = response.get_json()
#     assert data['nodes_with_highest_degree'] == [('A', 5), ('B', 4), ('C', 4)]

@patch('src.services.graph_services.GraphServices.all_paths')
def test_all_paths(mock_all_paths, client):
    # Configurar el mock
    mock_all_paths.return_value = {
        'paths': [['A', 'B', 'C'], ['A', 'D', 'C']]
    }

    # Llamar al endpoint
    response = client.get('/all-paths?origen=A&destino=C')

    # Verificaciones
    assert response.status_code == 200
    data = response.get_json()
    assert data['paths'] == [['A', 'B', 'C'], ['A', 'D', 'C']]
