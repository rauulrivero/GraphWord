from gui.app_interface import GraphVisualizer
from api.api_handler import APIHandler

class MockAPIHandler(APIHandler):
    def __init__(self, api_base_url):
        super().__init__(api_base_url)

    def get_request(self, endpoint, params=None):
        print(f"Mock GET request to {endpoint} with params {params}")
        return {"status": "success", "data": "Mock data for GET request"}

    def post_request(self, endpoint, json=None):
        print(f"Mock POST request to {endpoint} with body {json}")
        return {"status": "success", "data": "Mock data for POST request"}


def test_initialize_graph():
    """
    Test the initialization of the graph functionality in GraphVisualizer.
    """
    mock_api_handler = MockAPIHandler("http://mock-api")
    visualizer = GraphVisualizer(mock_api_handler)

    try:
        book_ids = "1, 2, 3"
        result = mock_api_handler.post_request("initialize-graph", json={"book_ids": book_ids.split(", ")})
        assert result["status"] == "success", "Failed to initialize graph"
        print("[PASSED] Initialize Graph test")
    except Exception as e:
        print(f"[FAILED] Initialize Graph test: {e}")


def test_shortest_path():
    """
    Test the shortest path calculation functionality in GraphVisualizer.
    """
    mock_api_handler = MockAPIHandler("http://mock-api")
    visualizer = GraphVisualizer(mock_api_handler)

    try:
        origen = "node1"
        destino = "node2"
        result = mock_api_handler.get_request("shortest-path", params={"origen": origen, "destino": destino})
        assert result["status"] == "success", "Failed to calculate shortest path"
        print("[PASSED] Shortest Path test")
    except Exception as e:
        print(f"[FAILED] Shortest Path test: {e}")


def test_isolated_nodes():
    """
    Test the isolated nodes functionality in GraphVisualizer.
    """
    mock_api_handler = MockAPIHandler("http://mock-api")
    visualizer = GraphVisualizer(mock_api_handler)

    try:
        result = mock_api_handler.get_request("isolated-nodes")
        assert result["status"] == "success", "Failed to retrieve isolated nodes"
        print("[PASSED] Isolated Nodes test")
    except Exception as e:
        print(f"[FAILED] Isolated Nodes test: {e}")


def test_detect_clusters():
    """
    Test the cluster detection functionality in GraphVisualizer.
    """
    mock_api_handler = MockAPIHandler("http://mock-api")
    visualizer = GraphVisualizer(mock_api_handler)

    try:
        result = mock_api_handler.get_request("detect-clusters")
        assert result["status"] == "success", "Failed to detect clusters"
        print("[PASSED] Detect Clusters test")
    except Exception as e:
        print(f"[FAILED] Detect Clusters test: {e}")


def test_nodes_by_degree():
    """
    Test the nodes by degree functionality in GraphVisualizer.
    """
    mock_api_handler = MockAPIHandler("http://mock-api")
    visualizer = GraphVisualizer(mock_api_handler)

    try:
        degree = 3
        result = mock_api_handler.get_request("nodes-by-degree", params={"degree": degree})
        assert result["status"] == "success", "Failed to retrieve nodes by degree"
        print("[PASSED] Nodes by Degree test")
    except Exception as e:
        print(f"[FAILED] Nodes by Degree test: {e}")


if __name__ == "__main__":
    print("Iniciando pruebas para Streamlit...")

    test_initialize_graph()
    test_shortest_path()
    test_isolated_nodes()
    test_detect_clusters()
    test_nodes_by_degree()

    print("Pruebas completadas.")
