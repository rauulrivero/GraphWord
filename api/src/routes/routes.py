from flask import Blueprint, jsonify, request, current_app, g
from src.services.graph_services import GraphServices
from src.aws.lambda_manager import LambdaManager
from dotenv import load_dotenv
import os

api = Blueprint('api', __name__)

load_dotenv()

CRAWLER_LAMBDA_URL = os.getenv('CRAWLER_LAMBDA_URL')
GRAPH_LAMBDA_URL = os.getenv('GRAPH_LAMBDA_URL')

lambda_manager = LambdaManager(CRAWLER_LAMBDA_URL, GRAPH_LAMBDA_URL)

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



@api.route('/initialize-graph', methods=['GET'])
def initialize_graph():
    """Inicializa un grafo descargando libros y generando el grafo."""
    # Obtener los IDs de libros de los parámetros de la solicitud
    book_ids = request.args.get('book_ids')

    if not book_ids:
        return jsonify({"error": "Debe proporcionar al menos un ID de libro en el parámetro 'book_ids'."}), 400

    # Convertir los IDs de libros en una lista
    book_ids_list = book_ids.split(',')

    # Añadir al final de los ids la extension .txt
    file_keys = [book_id + '.txt' for book_id in book_ids_list]

    try:
        # Llamar a la Lambda del Crawler
        lambda_manager.invoke_crawler(file_keys)

        # Llamar a la Lambda del Graph
        graph_result = lambda_manager.invoke_graph(file_keys)

        # Responder con los datos del grafo
        return jsonify({
            "message": "Grafo creado con éxito.",
            "graph_data": graph_result
        }), 200

    except RuntimeError as e:
        return jsonify({"error": "Error al procesar la solicitud.", "details": str(e)}), 500

    except Exception as e:
        return jsonify({"error": "Error inesperado.", "details": str(e)}), 500
