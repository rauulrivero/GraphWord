import os
import networkx as nx
import json

class FileManager:
    def __init__(self):
        pass

    def read_text_file(self, file_path):
        """
        Reads the content of a text file and returns it as a string.
        :param file_path: Path to the file.
        :return: File content as a string.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            return text
        except FileNotFoundError:
            print(f"The file {file_path} was not found.")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return None

    def get_files_in_folder(self, folder_path):
        """
        Retrieves all text files in the specified folder.

        :param folder_path: Path to the folder.
        :return: List of full paths to the files in the folder.
        """
        return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.txt')]
    
    
    def save_graph_to_json(self, graph, file_path):
        """
        Saves the graph in JSON format.

        Args:
            file_path (str): Path to the JSON file.
        """
        data = nx.node_link_data(graph)
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Graph successfully saved to {file_path}.")

    def load_graph_from_json(self, file_path):
        """
        Loads a graph from a JSON file.

        Args:
            file_path (str): Path to the JSON file.

        Returns:
            nx.Graph: Graph loaded from the file.
        """
        with open(file_path, 'r') as file:
            data = json.load(file)
        G = nx.node_link_graph(data)
        print(f"Graph successfully loaded from {file_path}.")
        return G
    
    # Create folder if it does not exist
    def create_folder(self, folder_path):
        """
        Creates a folder if it does not exist.

        Args:
            folder_path (str): Path of the folder to create.
        """
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"The folder {folder_path} has been created.")
        else:
            print(f"The folder {folder_path} already exists.")
