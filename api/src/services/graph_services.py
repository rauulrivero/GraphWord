import networkx as nx


class GraphServices:
    def __init__(self, graph):
        """
        Inicializa la API con un grafo.
        :param graph: Grafo de NetworkX sobre el cual se realizaran las operaciones.
        """
        self.graph = graph

    def shortest_path(self, start, end):
        """
        Calcula el camino más corto entre dos nodos usando el algoritmo de Dijkstra.
        :param start: Nodo de inicio.
        :param end: Nodo de destino.
        :return: Lista de nodos que forman el camino mas corto.
        """
        try:
            path = nx.shortest_path(self.graph, source=start, target=end, weight='weight')
            return {'path': path, 'length': nx.shortest_path_length(self.graph, source=start, target=end, weight='weight')}
        except nx.NetworkXNoPath:
            return {'error': 'No existe un camino entre los nodos especificados'}

    def all_paths(self, start, end):
            """
            Devuelve todos los caminos simples entre dos nodos sin pasar dos veces por el mismo nodo.
            :param start: Nodo de inicio.
            :param end: Nodo de destino.
            :return: Lista de caminos.
            """
            def dfs(current, target, visited, path):
                visited.add(current)
                path.append(current)

                if current == target:
                    paths.append(path[:])
                else:
                    for neighbor in self.graph.neighbors(current):
                        if neighbor not in visited:
                            dfs(neighbor, target, visited, path)

                visited.remove(current)
                path.pop()

            paths = []
            visited = set()
            dfs(start, end, visited, [])
            return {'paths': paths}

    def dfs_longest_path(self, start, end, visited=None, path=None):
            """
            Encuentra el camino más largo simple entre dos nodos usando DFS.
            :param start: Nodo inicial.
            :param end: Nodo final.
            :param visited: Conjunto de nodos visitados (para evitar ciclos).
            :param path: Camino actual (lista de nodos).
            :return: Camino más largo y su longitud.
            """
            if visited is None:
                visited = set()
            if path is None:
                path = []

            # Marca el nodo como visitado
            visited.add(start)
            path.append(start)

            if start == end:
                # Si llegamos al nodo final, devolvemos el camino actual
                return path[:]

            longest_path = []

            # Recorre los vecinos del nodo actual
            for neighbor in self.graph.neighbors(start):
                if neighbor not in visited:  # Evitar ciclos
                    candidate_path = self.dfs_longest_path(neighbor, end, visited, path)
                    if len(candidate_path) > len(longest_path):
                        longest_path = candidate_path

            # Desmarcar el nodo para otras exploraciones
            visited.remove(start)
            path.pop()

            return longest_path



    def detect_clusters(self):
        """
        Detecta clusteres densamente conectados en el grafo.
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
        Selecciona nodos con un numero especifico de conexiones.
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
