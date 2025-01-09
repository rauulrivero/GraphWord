import boto3
import json
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

class S3Manager:
    def __init__(self, region_name='us-east-1'):
        """
        Initialize the AWSManager with optional AWS credentials and region.
        """
        
        try:
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

    import boto3
import json
import os
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

    def download_file(self, bucket_name, object_key, temp_file_path):
        """
        Download a file from an S3 bucket and save it locally.

        :param bucket_name: The name of the S3 bucket.
        :param object_key: The key of the file to download.
        :param temp_file_path: The local path to save the downloaded file.
        :return: True if the file was downloaded successfully, False otherwise.
        """
        try:
            self.s3_client.download_file(bucket_name, object_key, temp_file_path)
            print(f"File '{object_key}' downloaded successfully to '{temp_file_path}'.")
            return True
        except self.s3_client.exceptions.NoSuchBucket:
            print(f"Bucket '{bucket_name}' does not exist.")
        except self.s3_client.exceptions.NoSuchKey:
            print(f"File '{object_key}' does not exist in bucket '{bucket_name}'.")
        except Exception as e:
            print(f"Error downloading file: {str(e)}")
        return False