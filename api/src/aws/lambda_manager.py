import boto3
import json

class LambdaManager:
    def __init__(self, crawler_function_name, graph_function_name, region_name='us-east-1'):
        """
        Inicializa el LambdaManager con los nombres de las funciones Lambda y la región de AWS.
        """
        self.lambda_client = boto3.client('lambda', region_name=region_name)
        self.crawler_function_name = crawler_function_name
        self.graph_function_name = graph_function_name

    def initialize_graph(self, book_ids_list, file_keys):
        """
        Inicializa el grafo llamando a las funciones Lambda para el Crawler y el Graph.
        """
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
        """
        Llama a la función Lambda del Crawler para descargar los libros.
        """
        payload = {"book_ids": book_ids}
        print(f"Enviando payload al Crawler: {payload}")

        try:
            response = self.lambda_client.invoke(
                FunctionName=self.crawler_function_name,
                InvocationType='RequestResponse',
                Payload=json.dumps(payload),
            )

            # Leer y procesar la respuesta
            response_payload = json.loads(response['Payload'].read())
            print(f"Crawler Response: {response_payload}")

            if response.get('StatusCode') != 200 or 'error' in response_payload:
                raise RuntimeError(f"Error en Lambda Crawler: {response_payload}")

            return response_payload
        except Exception as e:
            print(f"Error al llamar al Crawler: {e}")
            raise RuntimeError("No se pudo completar la solicitud al Crawler.")

    def invoke_graph(self, file_keys):
        """
        Llama a la función Lambda del Graph para generar el grafo.
        """
        payload = {"file_keys": file_keys}
        print(f"Enviando payload al Graph: {payload}")

        try:
            response = self.lambda_client.invoke(
                FunctionName=self.graph_function_name,
                InvocationType='RequestResponse',
                Payload=json.dumps(payload),
            )

            # Leer y procesar la respuesta
            response_payload = json.loads(response['Payload'].read())
            print(f"Graph Response: {response_payload}")

            if response.get('StatusCode') != 200 or 'error' in response_payload:
                raise RuntimeError(f"Error en Lambda Graph: {response_payload}")

            return response_payload
        except Exception as e:
            print(f"Error al llamar al Graph: {e}")
            raise RuntimeError("No se pudo completar la solicitud al Graph.")
