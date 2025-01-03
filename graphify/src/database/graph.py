import networkx as nx

# Function to check if two words differ by only one letter
def one_letter_difference(word1, word2):
    if len(word1) != len(word2):
        return False
    # Count how many letters are different
    difference = sum(1 for a, b in zip(word1, word2) if a != b)
    return difference == 1

# Function to generate the graph
def generate_graph(word_frequency_dict):
    """
    Generates a graph where nodes are words and edges have weights
    based on the frequencies of the words.

    Args:
        word_frequency_dict (dict): Dictionary with words as keys and frequencies as values.

    Returns:
        nx.Graph: Graph with words as nodes and weighted edges.
    """
    G = nx.Graph()  # Create an empty graph

    # Add nodes with frequency attributes
    for word, frequency in word_frequency_dict.items():
        G.add_node(word, frequency=frequency)

    # Compare each pair of words
    words = list(word_frequency_dict.keys())
    for i, word1 in enumerate(words):
        for word2 in words[i+1:]:  # Avoid duplicate comparisons
            if one_letter_difference(word1, word2):
                # Calculate the weight as the sum of frequencies divided by 2
                weight = (word_frequency_dict[word1] + word_frequency_dict[word2]) / 2
                G.add_edge(word1, word2, weight=weight)

    return G
