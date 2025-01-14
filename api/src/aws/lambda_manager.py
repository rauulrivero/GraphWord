import requests

class LambdaManager:
    def __init__(self, crawler_url, graph_url):
        self.crawler_url = crawler_url
        self.graph_url = graph_url

    def invoke_crawler(self, book_ids):
        """Llama a la Lambda del Crawler para descargar los libros."""
        response = requests.post(self.crawler_url, json={"book_ids": book_ids})
        if response.status_code != 200:
            raise RuntimeError(f"Error en Lambda Crawler: {response.json()}")
        return response.json()

    def invoke_graph(self, file_keys):
        """Llama a la Lambda del Graph para generar el grafo."""
        response = requests.post(self.graph_url, json={"file_keys": file_keys})
        if response.status_code != 200:
            raise RuntimeError(f"Error en Lambda Graph: {response.json()}")
        return response.json()