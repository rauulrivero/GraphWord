import networkx as nx
import json

class WordGraph:
    def __init__(self, word_frequency_dict):
        """
        Inicializa la clase con un diccionario de palabras y sus frecuencias.
        Genera un grafo donde los nodos son palabras y las aristas tienen pesos
        basados en las frecuencias de las palabras.

        Args:
            word_frequency_dict (dict): Diccionario con palabras como claves y frecuencias como valores.
        """
        self.word_frequency_dict = word_frequency_dict
        self.graph = self._generate_graph()

    def _one_letter_difference(self, word1, word2):
        """
        Verifica si dos palabras difieren en exactamente una letra.

        Args:
            word1 (str): Primera palabra.
            word2 (str): Segunda palabra.

        Returns:
            bool: True si las palabras difieren en una sola letra, False en caso contrario.
        """
        if len(word1) != len(word2):
            return False
        return sum(1 for a, b in zip(word1, word2) if a != b) == 1

    def _generate_graph(self):
        """
        Genera el grafo a partir del diccionario de frecuencias.

        Returns:
            nx.Graph: Grafo generado.
        """
        G = nx.Graph()

        # Añadir nodos con atributos de frecuencia
        for word, frequency in self.word_frequency_dict.items():
            G.add_node(word, frequency=frequency)

        # Añadir aristas entre palabras con diferencia de una letra
        words = list(self.word_frequency_dict.keys())
        for i, word1 in enumerate(words):
            for word2 in words[i+1:]:
                if self._one_letter_difference(word1, word2):
                    weight = (self.word_frequency_dict[word1] + self.word_frequency_dict[word2]) / 2
                    G.add_edge(word1, word2, weight=weight)

        return G

    def get_graph(self):
        """
        Devuelve el grafo generado.

        Returns:
            nx.Graph: Grafo de palabras.
        """
        return self.graph

    def get_neighbors(self, word):
        """
        Devuelve los vecinos de una palabra en el grafo.

        Args:
            word (str): Palabra para la que se quieren encontrar vecinos.

        Returns:
            list: Lista de palabras vecinas.
        """
        return list(self.graph.neighbors(word))

    def get_edge_weight(self, word1, word2):
        """
        Devuelve el peso de la arista entre dos palabras.

        Args:
            word1 (str): Primera palabra.
            word2 (str): Segunda palabra.

        Returns:
            float: Peso de la arista. None si no existe una arista.
        """
        if self.graph.has_edge(word1, word2):
            return self.graph[word1][word2]['weight']
        return None

    def display_graph_info(self):
        """
        Muestra información básica del grafo.
        """
        print("Número de nodos:", self.graph.number_of_nodes())
        print("Número de aristas:", self.graph.number_of_edges())
        print("Nodos con mayor grado:", sorted(self.graph.degree, key=lambda x: x[1], reverse=True)[:5])

    

