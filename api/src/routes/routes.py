from flask import Blueprint, jsonify, request
from src.services.graph_services import GraphServices
from src.database.word_graph import WordGraph

api = Blueprint('api', __name__)

graph = WordGraph()
graph_services = GraphServices(graph)

@api.route('/longest-path', methods=['GET'])
def longest_path():
    origen = request.args.get('origen')
    destino = request.args.get('destino')
    return graph_services.longest_path(origen, destino)

@api.route('/isolated-nodes', methods=['GET'])
def isolated_nodes():
    return graph_services.isolated_nodes()

@api.route('/nodes-with-highest-degree', methods=['GET'])
def nodes_with_highest_degree():
    return graph_services.nodes_with_highest_degree()

@api.route('/longest-path', methods=['GET'])
def longest_distance():
    return graph_services.longest_path()

@api.route('/all-paths', methods=['GET'])
def all_paths():
    origen = request.args.get('origen')
    destino = request.args.get('destino')
    return graph_services.all_paths(origen, destino)

@api.route('/detect-clusters', methods=['GET'])
def dense_subgraphs():
    return graph_services.detect_clusters()

@api.route('/nodes-by-degree', methods=['GET'])
def nodes_by_degree():
    degree = request.args.get('degree')
    return graph_services.nodes_by_degree(degree)
