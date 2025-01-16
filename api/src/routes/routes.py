from flask import Blueprint, jsonify, request, current_app, g
from src.services.graph_services import GraphServices
from src.aws.lambda_manager import LambdaManager
from src.aws.s3_manager import S3Manager
from src.database.graph import WordGraph
import json
from dotenv import load_dotenv
from networkx import Graph  # Ejemplo usando NetworkX
import os

api = Blueprint('api', __name__)




@api.before_request
def before_request():
    if not hasattr(current_app, 'graph') or current_app.graph is None:
        current_app.graph = Graph()
        print("Graph was not initialized. Initializing an empty graph.")
    
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



@api.route('/update-graph', methods=['POST'])
def update_graph():
    """Actualiza el grafo descargando libros, generando el grafo y cargándolo en la aplicación."""
    # Obtener los IDs de libros del cuerpo de la solicitud
    data = request.get_json()

    load_dotenv()

    CRAWLER_LAMBDA_URL = os.getenv('CRAWLER_LAMBDA_URL')
    GRAPH_LAMBDA_URL = os.getenv('GRAPH_LAMBDA_URL')
    S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
    JSON_FILE_KEY = os.getenv('JSON_FILE_KEY')

    lambda_manager = LambdaManager(CRAWLER_LAMBDA_URL, GRAPH_LAMBDA_URL)
    aws_manager = S3Manager()

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

    # Inicializar el grafo utilizando Lambda
    lambda_manager.initialize_graph(book_ids_list, file_keys)

    try:
        # Descargar el grafo actualizado desde S3
        json_content = aws_manager.get_object_content(S3_BUCKET_NAME, JSON_FILE_KEY)

        if json_content:
            # Parsear el contenido JSON y actualizar el grafo en la app
            json_graph = json.loads(json_content)
            word_graph = WordGraph(json_graph)
            current_app.graph = word_graph.get_graph()
            return jsonify({"message": "Grafo actualizado y cargado en la aplicación con éxito."}), 200
        else:
            return jsonify({"error": "No se pudo descargar el grafo desde S3."}), 500
    except Exception as e:
        print(f"An error occurred while updating the graph: {e}")
        return jsonify({"error": f"Ocurrió un error al actualizar el grafo: {e}"}), 500

