from src.controller import Controller


DATALAKE_BUCKET = 'books-datalake'
GRAPH_BUCKET = 'books-graph'
S3_BUCKET_PATH = 'graph.json'


def lambda_handler(event, context):
    """
    AWS Lambda handler function to execute the controller logic.

    Args:
        event (dict): Event data passed to the Lambda function.
        context (object): Runtime information passed to the Lambda function.

    Returns:
        dict: A response indicating success or failure.
    """
    try:

        file_keys = event.get("file_keys", [])

        controller = Controller(DATALAKE_BUCKET, GRAPH_BUCKET, file_keys, S3_BUCKET_PATH)
        controller.run()

        return {
            'statusCode': 200,
            'body': 'Controller executed successfully.'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error occurred: {str(e)}'
        }
