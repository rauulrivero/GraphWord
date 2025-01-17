import networkx as nx

class WordGraph:
    def __init__(self, word_frequency_dict):
        self.word_frequency_dict = word_frequency_dict
        self.graph = self._generate_graph()

    def _one_letter_difference(self, word1, word2):
        if len(word1) != len(word2):
            return False
        return sum(1 for a, b in zip(word1, word2) if a != b) == 1

    def _generate_graph(self):
        G = nx.Graph()
        for word, frequency in self.word_frequency_dict.items():
            G.add_node(word, frequency=frequency)
        words = list(self.word_frequency_dict.keys())
        for i, word1 in enumerate(words):
            for word2 in words[i+1:]:
                if self._one_letter_difference(word1, word2):
                    weight = (self.word_frequency_dict[word1] + self.word_frequency_dict[word2]) / 2
                    G.add_edge(word1, word2, weight=weight)
        return G

    def get_graph(self):
        return self.graph

    def get_neighbors(self, word):
        return list(self.graph.neighbors(word))

    def get_edge_weight(self, word1, word2):
        if self.graph.has_edge(word1, word2):
            return self.graph[word1][word2]['weight']
        return None

    def display_graph_info(self):
        print("Number of nodes:", self.graph.number_of_nodes())
        print("Number of edges:", self.graph.number_of_edges())
        print("Nodes with the highest degree:", sorted(self.graph.degree, key=lambda x: x[1], reverse=True)[:5])

    def to_json(self):
        return nx.node_link_data(self.graph, edges="links")
