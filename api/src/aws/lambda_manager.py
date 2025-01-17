import boto3
import json

class LambdaManager:
    def __init__(self, crawler_function_name, graph_function_name, region_name='us-east-1'):
        self.lambda_client = boto3.client('lambda', region_name=region_name)
        self.crawler_function_name = crawler_function_name
        self.graph_function_name = graph_function_name

    def initialize_graph(self, book_ids_list, file_keys):
        try:
            print(f"Initializing graph with book IDs: {book_ids_list}")
            self.invoke_crawler(book_ids_list)
            graph_result = self.invoke_graph(file_keys)
            return {
                "message": "Graph successfully created.",
                "graph_data": graph_result
            }
        except RuntimeError as e:
            print(f"RuntimeError: {e}")
            return {"error": "Error processing the request.", "details": str(e)}, 500
        except Exception as e:
            print(f"Unexpected error: {e}")
            return {"error": "Unexpected error.", "details": str(e)}, 500

    def invoke_crawler(self, book_ids):
        payload = {"book_ids": book_ids}
        print(f"Sending payload to Crawler: {payload}")
        try:
            response = self.lambda_client.invoke(
                FunctionName=self.crawler_function_name,
                InvocationType='RequestResponse',
                Payload=json.dumps(payload),
            )
            response_payload = json.loads(response['Payload'].read())
            print(f"Crawler Response: {response_payload}")
            if response.get('StatusCode') != 200 or 'error' in response_payload:
                raise RuntimeError(f"Error in Crawler Lambda: {response_payload}")
            return response_payload
        except Exception as e:
            print(f"Error calling Crawler: {e}")
            raise RuntimeError("Could not complete the request to the Crawler.")

    def invoke_graph(self, file_keys):
        payload = {"file_keys": file_keys}
        print(f"Sending payload to Graph: {payload}")
        try:
            response = self.lambda_client.invoke(
                FunctionName=self.graph_function_name,
                InvocationType='RequestResponse',
                Payload=json.dumps(payload),
            )
            response_payload = json.loads(response['Payload'].read())
            print(f"Graph Response: {response_payload}")
            if response.get('StatusCode') != 200 or 'error' in response_payload:
                raise RuntimeError(f"Error in Graph Lambda: {response_payload}")
            return response_payload
        except Exception as e:
            print(f"Error calling Graph: {e}")
            raise RuntimeError("Could not complete the request to the Graph.")
