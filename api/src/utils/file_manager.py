import json

class FileManager:
    def __init__(self):
        pass

    def read_json(self, file_path):
        """
        Lee un archivo JSON y devuelve su contenido.
        :param file_path: Ruta al archivo JSON.
        :return: Contenido del archivo JSON.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as json_file:
                return json.load(json_file)
        except Exception as e:
            print(f"Ocurrio un error al leer el archivo JSON: {e}")
            return None
