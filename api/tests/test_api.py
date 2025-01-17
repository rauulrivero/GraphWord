import pytest
from unittest.mock import MagicMock, patch
from flask import Flask
from api.src import create_app
from api.src.routes.routes import api
from api.src.services.graph_services import GraphServices
import json


@pytest.fixture
def client():

    app = create_app()
    app.register_blueprint(api)
    app.testing = True

    mock_graph = MagicMock()
    app.graph = mock_graph

    return app.test_client()

@patch('src.services.graph_services.GraphServices.shortest_path')
def test_shortest_path(mock_shortest_path, client):

    mock_shortest_path.return_value = {
        'path': ['A', 'B', 'C'],
        'length': 2
    }

    response = client.get('/shortest-path?origen=A&destino=C')

    assert response.status_code == 200
    data = response.get_json()
    assert data['path'] == ['A', 'B', 'C']
    assert data['length'] == 2

@patch('src.services.graph_services.GraphServices.isolated_nodes')
def test_isolated_nodes(mock_isolated_nodes, client):
    
    mock_isolated_nodes.return_value = {
        'isolated_nodes': ['X', 'Y', 'Z']
    }

    response = client.get('/isolated-nodes')

    assert response.status_code == 200
    data = response.get_json()
    assert data['isolated_nodes'] == ['X', 'Y', 'Z']

@patch('src.services.graph_services.GraphServices.detect_clusters')
def test_detect_clusters(mock_detect_clusters, client):

    mock_detect_clusters.return_value = {
        'clusters': [['A', 'B'], ['C', 'D', 'E']]
    }

    response = client.get('/detect-clusters')

    assert response.status_code == 200
    data = response.get_json()
    assert data['clusters'] == [['A', 'B'], ['C', 'D', 'E']]


@patch('src.services.graph_services.GraphServices.all_paths')
def test_all_paths(mock_all_paths, client):

    mock_all_paths.return_value = {
        'paths': [['A', 'B', 'C'], ['A', 'D', 'C']]
    }

    response = client.get('/all-paths?origen=A&destino=C')

    assert response.status_code == 200
    data = response.get_json()
    assert data['paths'] == [['A', 'B', 'C'], ['A', 'D', 'C']]
