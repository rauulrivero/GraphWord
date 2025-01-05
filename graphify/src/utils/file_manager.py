import os
import networkx as nx
import json

class FileManager:
    def read_text_file(self, file_path):
        """
        Lee el contenido de un archivo de texto y lo devuelve como un string.
        :param file_path: Ruta al archivo.
        :return: Contenido del archivo como un string.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text = file.read()
            return text
        except FileNotFoundError:
            print(f"El archivo {file_path} no se encontró.")
        except Exception as e:
            print(f"Ocurrió un error al leer el archivo: {e}")
            return None

    def get_files_in_folder(self, folder_path):
        """
        Obtiene todos los archivos de texto en la carpeta especificada.

        :param folder_path: Ruta a la carpeta.
        :return: Lista de rutas completas a los archivos en la carpeta.
        """
        return [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.txt')]
    
    
    def save_graph_to_json(self, graph, file_path):
        """
        Guarda el grafo en formato JSON.

        Args:
            file_path (str): Ruta al archivo JSON.
        """
        data = nx.node_link_data(graph)
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Grafo guardado correctamente en {file_path}.")

    def load_graph_from_json(self, file_path):
        """
        Carga un grafo desde un archivo JSON.

        Args:
            file_path (str): Ruta al archivo JSON.

        Returns:
            nx.Graph: Grafo cargado desde el archivo.
        """
        with open(file_path, 'r') as file:
            data = json.load(file)
        G = nx.node_link_graph(data)
        print(f"Grafo cargado correctamente desde {file_path}.")
        return G
    