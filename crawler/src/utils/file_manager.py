import os

class FileManager:
    def __init__(self, base_path=None):
        """
        Inicializa el gestor de archivos.

        :param base_path: Ruta base donde se gestionarán los archivos. Opcional.
        """
        self.base_path = base_path

    def save_text_to_file(self, text, file_path):
        """
        Guarda el texto en un archivo especificado.

        :param text: Texto a guardar.
        :param file_path: Ruta completa del archivo donde se guardará el texto.
        """
        try:
            # Si base_path está configurado, combina con file_path
            full_path = os.path.join(self.base_path, file_path) if self.base_path else file_path

            # Asegurarse de que el directorio existe
            directory = os.path.dirname(full_path)
            if directory:
                os.makedirs(directory, exist_ok=True)

            # Escribir el texto en el archivo
            with open(full_path, 'w', encoding='utf-8') as file:
                file.write(text)
                print(f"Texto guardado correctamente en {full_path}.")
        except Exception as e:
            print(f"Error al guardar el texto en {file_path}: {e}")

    def read_text_from_file(self, file_path):
        """
        Lee y devuelve el contenido de un archivo.

        :param file_path: Ruta completa del archivo a leer.
        :return: Contenido del archivo como string.
        """
        try:
            # Si base_path está configurado, combina con file_path
            full_path = os.path.join(self.base_path, file_path) if self.base_path else file_path

            # Leer el contenido del archivo
            with open(full_path, 'r', encoding='utf-8') as file:
                content = file.read()
                print(f"Archivo leído correctamente desde {full_path}.")
                return content
        except FileNotFoundError:
            print(f"Error: El archivo {file_path} no existe.")
            return None
        except Exception as e:
            print(f"Error al leer el archivo {file_path}: {e}")
            return None
