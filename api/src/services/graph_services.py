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
        Calcula el camino más largo entre dos nodos, permitiendo ciclos.
        :param start: Nodo de inicio.
        :param end: Nodo de destino.
        :return: Lista de nodos que forman el camino más largo y su longitud.
        """
        try:
            # Encuentra todos los caminos simples entre start y end
            all_paths = list(nx.all_simple_paths(self.graph, source=start, target=end))

            # Si no se encuentra ningún camino
            if not all_paths:
                return {'error': 'No hay caminos entre los nodos proporcionados'}
            
            # Encuentra el camino más largo (por número de nodos en el camino)
            longest_path = max(all_paths, key=len)
            
            # Calcular la longitud del camino (sumando los pesos de las aristas, si los hay)
            length = sum(self.graph[u][v].get('weight', 1) for u, v in zip(longest_path[:-1], longest_path[1:]))
            
            return {'path': longest_path, 'length': length}
        except Exception as e:
            return {'error': str(e)}


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
        :return: Lista de los 15 nodos con mayor grado ordenados por grado descendente.
        """
        nodes = sorted(self.graph.degree, key=lambda x: x[1], reverse=True)
        
        # Limitar a los 15 nodos con mayor grado
        top_15_nodes = nodes[:15]
        
        return {'nodes_with_highest_degree': top_15_nodes}

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
