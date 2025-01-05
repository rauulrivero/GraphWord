import networkx as nx

class WordGraph:
    def __init__(self, json_data=None):
        """
        Inicializa la clase WordGraph, cargando un grafo a partir de un diccionario de datos JSON.

        :param json_data: Diccionario que contiene los datos del grafo.
        """
        self.graph = nx.Graph()

        if json_data:
            self.load_graph_from_json_data(json_data)

    def load_graph_from_json_data(self, json_data):
        """
        Carga un grafo a partir de un diccionario de datos JSON.

        :param json_data: Diccionario que contiene los datos del grafo en formato node-link.
        """
        try:
            self.graph = nx.node_link_graph(json_data)  # Convertir los datos en un grafo de NetworkX
            print("Grafo cargado correctamente.")
        except Exception as e:
            print(f"Ocurrió un error al cargar los datos JSON: {e}")

    def display_graph_info(self):
        """
        Muestra información básica del grafo.
        """
        print(f"Número de nodos: {self.graph.number_of_nodes()}")
        print(f"Número de aristas: {self.graph.number_of_edges()}")
        print("Algunos nodos:", list(self.graph.nodes)[:5])  # Muestra los primeros 5 nodos

    def get_graph(self):
        """
        Devuelve el grafo de NetworkX.

        :return: Objeto NetworkX Graph.
        """
        return self.graph
