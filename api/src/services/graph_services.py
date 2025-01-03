import networkx as nx


class GraphServices:
    def __init__(self, graph):
        """
        Inicializa la API con un grafo.
        :param graph: Grafo de NetworkX sobre el cual se realizarán las operaciones.
        """
        self.graph = graph

    def shortest_path(self, start, end):
        """
        Calcula el camino más corto entre dos nodos usando el algoritmo de Dijkstra.
        :param start: Nodo de inicio.
        :param end: Nodo de destino.
        :return: Lista de nodos que forman el camino más corto.
        """
        try:
            path = nx.shortest_path(self.graph, source=start, target=end, weight='weight')
            return {'path': path, 'length': nx.shortest_path_length(self.graph, source=start, target=end, weight='weight')}
        except nx.NetworkXNoPath:
            return {'error': 'No existe un camino entre los nodos especificados'}

    def all_paths(self, start, end):
        """
        Devuelve todos los caminos simples entre dos nodos.
        :param start: Nodo de inicio.
        :param end: Nodo de destino.
        :return: Lista de caminos.
        """
        try:
            paths = list(nx.all_simple_paths(self.graph, source=start, target=end))
            return {'paths': paths}
        except nx.NetworkXNoPath:
            return {'error': 'No existe un camino entre los nodos especificados'}

    def longest_path(self, start, end):
        """
        Calcula el camino más largo sin ciclos entre dos nodos.
        :param start: Nodo de inicio.
        :param end: Nodo de destino.
        :return: Lista de nodos que forman el camino más largo y su longitud.
        """
        if nx.is_directed_acyclic_graph(self.graph):
            path = nx.dag_longest_path(self.graph)
            length = sum(self.graph[u][v].get('weight', 1) for u, v in zip(path[:-1], path[1:]))
            return {'path': path, 'length': length}
        else:
            return {'error': 'El grafo tiene ciclos, no se puede calcular el camino más largo'}

    def detect_clusters(self):
        """
        Detecta clústeres densamente conectados en el grafo.
        :return: Lista de cliques (subgrafos densamente conectados).
        """
        cliques = list(nx.find_cliques(self.graph))
        return {'clusters': cliques}

    def nodes_with_highest_degree(self):
        """
        Identifica los nodos con mayor grado de conectividad.
        :return: Lista de nodos ordenados por grado descendente.
        """
        nodes = sorted(self.graph.degree, key=lambda x: x[1], reverse=True)
        return {'nodes_with_highest_degree': nodes}

    def nodes_by_degree(self, degree):
        """
        Selecciona nodos con un número específico de conexiones.
        :param degree: Número de conexiones deseado.
        :return: Lista de nodos con ese grado de conectividad.
        """
        nodes = [node for node, deg in self.graph.degree if deg == degree]
        return {'nodes_with_degree': nodes}

    def isolated_nodes(self):
        """
        Devuelve los nodos sin conexiones en el grafo.
        :return: Lista de nodos aislados.
        """
        nodes = list(nx.isolates(self.graph))
        return {'isolated_nodes': nodes}
