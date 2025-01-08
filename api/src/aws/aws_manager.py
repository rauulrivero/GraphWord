import boto3

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
        Download a file from an S3 bucket.

        :param bucket_name: The name of the S3 bucket.
        :param object_key: The key of the file to download.
        :param file_path: The local path to save the downloaded file.
        :return: True if the file was downloaded successfully, False otherwise.
        """
        try:
            self.s3_client.download_file(bucket_name, object_key, file_path)
            print(f"File '{object_key}' downloaded successfully to '{file_path}'.")
            return True
        except self.s3_client.exceptions.NoSuchBucket:
            print(f"Bucket '{bucket_name}' does not exist.")
        except self.s3_client.exceptions.NoSuchKey:
            print(f"File '{object_key}' does not exist in bucket '{bucket_name}'.")
        except Exception as e:
            print(f"Error downloading file: {str(e)}")
        return False
