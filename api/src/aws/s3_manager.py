import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

class S3Manager:
    def __init__(self, region_name='us-east-1'):
        """
        Initialize the S3Manager with optional AWS credentials and region.
        """
        try:
            self.s3_client = boto3.client('s3', region_name=region_name)
        except (NoCredentialsError, PartialCredentialsError) as e:
            print("Error initializing S3Manager: ", str(e))
            raise

    def get_object_content(self, bucket_name, object_key):
        """
        Download a file from an S3 bucket and return its content as a string.

        :param bucket_name: The name of the S3 bucket.
        :param object_key: The key of the file to download.
        :return: The content of the file as a string, or None if an error occurs.
        """
        try:
            print(f"Attempting to download file '{object_key}' from bucket '{bucket_name}'...")
            response = self.s3_client.get_object(Bucket=bucket_name, Key=object_key)
            content = response['Body'].read().decode('utf-8')
            print(f"File '{object_key}' downloaded successfully from bucket '{bucket_name}'.")
            return content

        except self.s3_client.exceptions.NoSuchBucket:
            print(f"Error: Bucket '{bucket_name}' does not exist.")
        except self.s3_client.exceptions.NoSuchKey:
            print(f"Error: File '{object_key}' does not exist in bucket '{bucket_name}'.")
        except self.s3_client.exceptions.ClientError as e:
            error_code = e.response['Error']['Code']
            print(f"ClientError: {error_code} while accessing bucket '{bucket_name}' or file '{object_key}'.")
        except Exception as e:
            print(f"Unexpected error occurred while downloading file: {str(e)}")
        
        return None
