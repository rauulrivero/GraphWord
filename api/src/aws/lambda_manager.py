import requests

class LambdaManager:
    def __init__(self, crawler_url, graph_url):
        self.crawler_url = crawler_url
        self.graph_url = graph_url

    def initialize_graph(self, book_ids_list, file_keys):
        try:
            print(f"Initializing graph with book IDs: {book_ids_list}")
            # Llamar a la Lambda del Crawler
            self.invoke_crawler(book_ids_list)

            # Llamar a la Lambda del Graph
            graph_result = self.invoke_graph(file_keys)

            # Responder con los datos del grafo
            return {
                "message": "Grafo creado con éxito.",
                "graph_data": graph_result
            }
        except RuntimeError as e:
            print(f"RuntimeError: {e}")
            return {"error": "Error al procesar la solicitud.", "details": str(e)}, 500
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {"error": "Error inesperado.", "details": str(e)}, 500



    def invoke_crawler(self, book_ids):
        """Llama a la Lambda del Crawler para descargar los libros."""
        print({"book_ids": book_ids})
        response = requests.post(self.crawler_url, json={"body": {"book_ids": book_ids}})
        print(f"Crawler Response: {response.status_code}, {response.text}")
        if response.status_code != 200:
            raise RuntimeError(f"Error en Lambda Crawler: {response.json()}")

        if response.status_code != 200:
            raise RuntimeError(f"Error en Lambda Crawler: {response.json()}")
        return response.json()

    def invoke_graph(self, file_keys):
        """Llama a la Lambda del Graph para generar el grafo."""
        response = requests.post(self.graph_url, json={"file_keys": file_keys})
        if response.status_code != 200:
            raise RuntimeError(f"Error en Lambda Graph: {response.json()}")
        return response.json()
    
  