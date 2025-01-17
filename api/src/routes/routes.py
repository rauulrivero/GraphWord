from flask import Blueprint, jsonify, request, current_app, g
from src.services.graph_services import GraphServices
from src.aws.lambda_manager import LambdaManager
from src.aws.s3_manager import S3Manager
from src.database.graph import WordGraph
import json
from dotenv import load_dotenv
import os

api = Blueprint('api', __name__)

@api.before_request
def before_request():
    try:
        if not hasattr(current_app, 'graph') or current_app.graph is None:
            current_app.graph = WordGraph().get_graph()
            print("Graph was not initialized. Initializing an empty graph.")
        g.graph_services = GraphServices(current_app.graph)
    except Exception as e:
        print(f"Error during before_request setup: {e}")
        return jsonify({"error": "Failed to initialize graph services.", "details": str(e)}), 500

@api.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'Welcome to the graph API!'})

@api.route('/shortest-path', methods=['GET'])
def shortest_path():
    try:
        source = request.args.get('source')
        target = request.args.get('target')
        return g.graph_services.shortest_path(source, target)
    except KeyError as e:
        return jsonify({"error": "Missing required parameter.", "details": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error finding shortest path.", "details": str(e)}), 500

@api.route('/isolated-nodes', methods=['GET'])
def isolated_nodes():
    try:
        return g.graph_services.isolated_nodes()
    except Exception as e:
        return jsonify({"error": "Error fetching isolated nodes.", "details": str(e)}), 500

@api.route('/longest-path', methods=['GET'])
def longest_path():
    try:
        source = request.args.get('source')
        target = request.args.get('target')
        return g.graph_services.dfs_longest_path(source, target)
    except KeyError as e:
        return jsonify({"error": "Missing required parameter.", "details": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error finding longest path.", "details": str(e)}), 500

@api.route('/nodes-with-highest-degree', methods=['GET'])
def nodes_with_highest_degree():
    try:
        return g.graph_services.nodes_with_highest_degree()
    except Exception as e:
        return jsonify({"error": "Error fetching nodes with highest degree.", "details": str(e)}), 500

@api.route('/longest-path', methods=['GET'])
def longest_distance():
    try:
        return g.graph_services.longest_path()
    except Exception as e:
        return jsonify({"error": "Error calculating longest distance.", "details": str(e)}), 500

@api.route('/all-paths', methods=['GET'])
def all_paths():
    try:
        source = request.args.get('source')
        target = request.args.get('target')
        return g.graph_services.all_paths(source, target)
    except KeyError as e:
        return jsonify({"error": "Missing required parameter.", "details": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error fetching all paths.", "details": str(e)}), 500

@api.route('/detect-clusters', methods=['GET'])
def dense_subgraphs():
    try:
        return g.graph_services.detect_clusters()
    except Exception as e:
        return jsonify({"error": "Error detecting clusters.", "details": str(e)}), 500

@api.route('/nodes-by-degree', methods=['GET'])
def nodes_by_degree():
    try:
        degree = int(request.args.get('degree'))
        return g.graph_services.nodes_by_degree(degree)
    except ValueError as e:
        return jsonify({"error": "Invalid degree value.", "details": str(e)}), 400
    except Exception as e:
        return jsonify({"error": "Error fetching nodes by degree.", "details": str(e)}), 500

@api.route('/create-graph', methods=['POST'])
def create_graph():
    try:
        load_dotenv()
        data = request.get_json()
        CRAWLER_FUNCTION_NAME = os.getenv('CRAWLER_LAMBDA_NAME')
        GRAPH_FUNCTION_NAME = os.getenv('GRAPH_LAMBDA_NAME')
        GRAPH_BUCKET_NAME = os.getenv('GRAPH_BUCKET_NAME')
        JSON_FILE_KEY = os.getenv('JSON_FILE_KEY')

        lambda_manager = LambdaManager(
            crawler_function_name=CRAWLER_FUNCTION_NAME,
            graph_function_name=GRAPH_FUNCTION_NAME
        )
        aws_manager = S3Manager()

        book_ids_list = data.get('book_ids', [])
        min_len = data.get('min_len')
        max_len = data.get('max_len')

        # Validate book_ids_list
        if not isinstance(book_ids_list, list) or not all(isinstance(book_id, int) for book_id in book_ids_list):
            return jsonify({"error": "The 'book_ids' field must be a list of integers."}), 400

        # Validate min_len and max_len
        if not isinstance(min_len, int) or not isinstance(max_len, int):
            return jsonify({"error": "The 'min_len' and 'max_len' fields must be integers."}), 400
        
        if min_len <= 0 or max_len <= 0 or min_len > max_len:
            return jsonify({"error": "Invalid values for 'min_len' and 'max_len'. Ensure min_len > 0, max_len > 0, and min_len <= max_len."}), 400

        file_keys = [f"{book_id}.txt" for book_id in book_ids_list]
        print(f"File keys generated: {file_keys}")

        # Pass min_len and max_len to initialize_graph
        lambda_manager.initialize_graph(book_ids_list, file_keys, min_len, max_len)
        json_content = aws_manager.get_object_content(GRAPH_BUCKET_NAME, JSON_FILE_KEY)

        if json_content:
            json_graph = json.loads(json_content)
            word_graph = WordGraph(json_graph)
            current_app.graph = word_graph.get_graph()
            return jsonify({"message": "Graph successfully updated and loaded into the application."}), 200
        else:
            return jsonify({"error": "Could not download the graph from S3."}), 500

    except KeyError as e:
        return jsonify({"error": "Missing environment variable.", "details": str(e)}), 500
    except RuntimeError as e:
        print(f"RuntimeError occurred: {e}")
        return jsonify({"error": "Error processing the request.", "details": str(e)}), 500
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500
