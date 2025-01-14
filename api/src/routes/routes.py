from flask import Blueprint, jsonify, request, current_app, g
from src.services.graph_services import GraphServices
from src.aws.lambda_manager import LambdaManager
from dotenv import load_dotenv
import os

api = Blueprint('api', __name__)


@api.before_request
def before_request():
    g.graph_services = GraphServices(current_app.graph)

@api.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to the graph API!'})

@api.route('/shortest-path', methods=['GET'])
def shortest_path():
    origen = request.args.get('origen')
    destino = request.args.get('destino')
    return g.graph_services.shortest_path(origen, destino)

@api.route('/isolated-nodes', methods=['GET'])
def isolated_nodes():
    return g.graph_services.isolated_nodes()


@api.route('/longest-path', methods=['GET'])
def longest_path():
    origen = request.args.get('origen')
    destino = request.args.get('destino')
    return g.graph_services.longest_path(origen, destino)


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
    degree = int(request.args.get('degree'))
    return g.graph_services.nodes_by_degree(degree)



@api.route('/initialize-graph', methods=['POST'])
def initialize_graph():
    """Inicializa un grafo descargando libros y generando el grafo."""
    # Obtener los IDs de libros del cuerpo de la solicitud
    data = request.get_json()

    load_dotenv()

    CRAWLER_LAMBDA_URL = os.getenv('CRAWLER_LAMBDA_URL')
    GRAPH_LAMBDA_URL = os.getenv('GRAPH_LAMBDA_URL')

    lambda_manager = LambdaManager(CRAWLER_LAMBDA_URL, GRAPH_LAMBDA_URL)


    if not data or 'book_ids' not in data:
        return jsonify({"error": "Debe proporcionar una lista de IDs de libros en el cuerpo de la solicitud con la clave 'book_ids'."}), 400

    # Convertir los IDs de libros en una lista
    book_ids_list = data['book_ids']

    print(book_ids_list)

    if not isinstance(book_ids_list, list) or not all(isinstance(book_id, str) for book_id in book_ids_list):
        return jsonify({"error": "El campo 'book_ids' debe ser una lista de cadenas."}), 400

    # Añadir al final de los ids la extensión .txt
    file_keys = [book_id + '.txt' for book_id in book_ids_list]
    print(file_keys)

    lambda_manager.initialize_graph(book_ids_list, file_keys)

    return jsonify({"message": "Grafo creado con éxito."}), 200
