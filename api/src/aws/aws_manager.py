import boto3
import json
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

class AWSManager:
    def __init__(self, aws_access_key=None, aws_secret_key=None, region_name='us-east-1'):
        """
        Initialize the AWSManager with optional AWS credentials and region.
        """
        
        try:
            if aws_access_key and aws_secret_key:
                self.s3_client = boto3.client(
                    's3',
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key,
                    region_name=region_name
                )
            else:
                # Use default credentials (e.g., from environment or IAM role)
                self.s3_client = boto3.client('s3', region_name=region_name)
        except (NoCredentialsError, PartialCredentialsError) as e:
            print("Error initializing AWSManager: ", str(e))
            raise

    def list_bucket_contents(self, bucket_name):
        """
        List the contents of an S3 bucket.

        :param bucket_name: The name of the S3 bucket.
        :return: A list of objects in the bucket or an error message.
        """
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name)
            
            if 'Contents' in response:
                objects = [obj['Key'] for obj in response['Contents']]
                return objects
            else:
                return []  # Empty bucket

        except self.s3_client.exceptions.NoSuchBucket:
            print(f"Bucket '{bucket_name}' does not exist.")
            return None
        except Exception as e:
            print(f"Error listing bucket contents: {str(e)}")
            return None

    def download_file(self, bucket_name, object_key, file_path):
        """
        Download a JSON file from an S3 bucket using get_object.

        :param bucket_name: The name of the S3 bucket.
        :param object_key: The key of the file to download.
        :param file_path: The local path to save the downloaded file.
        :return: The parsed JSON object if downloaded and parsed successfully, None otherwise.
        """
        try:
            response = self.s3_client.get_object(Bucket=bucket_name, Key=object_key)

            # Read and decode the content of the file
            content = response['Body'].read().decode('utf-8')
            json_data = json.loads(content)

            # Optionally save the JSON content to a file
            with open(file_path, 'w') as file:
                json.dump(json_data, file, indent=4)

            print(f"File '{object_key}' downloaded and saved successfully to '{file_path}'.")
            return json_data
        except self.s3_client.exceptions.NoSuchBucket:
            print(f"Bucket '{bucket_name}' does not exist.")
        except self.s3_client.exceptions.NoSuchKey:
            print(f"File '{object_key}' does not exist in bucket '{bucket_name}'.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON content: {str(e)}")
        except Exception as e:
            print(f"Error downloading file: {str(e)}")
        return None
