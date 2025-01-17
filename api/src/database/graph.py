import networkx as nx

class WordGraph:
    def __init__(self, json_data=None):
        self.graph = nx.Graph()
        if json_data:
            self.load_graph_from_json_data(json_data)

    def load_graph_from_json_data(self, json_data):
        try:
            self.graph = nx.node_link_graph(json_data)
            print("Graph successfully loaded.")
        except Exception as e:
            print(f"An error occurred while loading JSON data: {e}")

    def display_graph_info(self):
        print(f"Number of nodes: {self.graph.number_of_nodes()}")
        print(f"Number of edges: {self.graph.number_of_edges()}")
        print("Some nodes:", list(self.graph.nodes)[:5])

    def get_graph(self):
        return self.graph
