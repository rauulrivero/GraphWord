from flask import Blueprint, jsonify, request, current_app, g
from src.services.graph_services import GraphServices

api = Blueprint('api', __name__)

@api.before_request
def before_request():
    # Inicializamos GraphServices una vez por solicitud
    g.graph_services = GraphServices(current_app.graph)

@api.route('/graph-info', methods=['GET'])
def graph_info():
    return g.graph_services.graph_info()

@api.route('/shortest-path', methods=['GET'])
def shortest_path():
    origen = request.args.get('origen')
    destino = request.args.get('destino')
    return g.graph_services.shortest_path(origen, destino)


@api.route('/longest-path', methods=['GET'])
def longest_path():
    origen = request.args.get('origen')
    destino = request.args.get('destino')
    return g.graph_services.longest_path(origen, destino)

@api.route('/isolated-nodes', methods=['GET'])
def isolated_nodes():
    return g.graph_services.isolated_nodes()

@api.route('/nodes-with-highest-degree', methods=['GET'])
def nodes_with_highest_degree():
    return g.graph_services.nodes_with_highest_degree()

@api.route('/longest-path', methods=['GET'])
def longest_distance():
    return g.graph_services.longest_path()

@api.route('/all-paths', methods=['GET'])
def all_paths():
    origen = request.args.get('origen')
    destino = request.args.get('destino')
    return g.graph_services.all_paths(origen, destino)

@api.route('/detect-clusters', methods=['GET'])
def dense_subgraphs():
    return g.graph_services.detect_clusters()

@api.route('/nodes-by-degree', methods=['GET'])
def nodes_by_degree():
    degree = request.args.get('degree')
    return g.graph_services.nodes_by_degree(degree)
