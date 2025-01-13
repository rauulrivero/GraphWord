import boto3
import json
import os

class S3Manager:
    def __init__(self, region_name):
        self.s3_client = boto3.client('s3', region_name=region_name)

    def download_txt_files_to_memory(self, bucket_name, s3_keys):
        """
        Downloads all .txt files from a specified S3 bucket and stores their content in memory.

        :param bucket_name: Name of the S3 bucket.
        :return: Dictionary with book IDs as keys and file content as values.
        """
        try:

            books_in_memory = {}
            for file_key in s3_keys:
                if file_key.endswith('.txt'):
                    file_obj = self.s3_client.get_object(Bucket=bucket_name, Key=file_key)
                    file_content = file_obj['Body'].read().decode('utf-8')
                    book_id = os.path.splitext(os.path.basename(file_key))[0]
                    books_in_memory[book_id] = file_content

            return books_in_memory

        except Exception as e:
            print(f"Error downloading files: {str(e)}")
            return {}
        


    def upload_json_file(self, bucket_name, json_data, s3_key):
        """
        Uploads a JSON object to a specified S3 bucket.

        :param bucket_name: Name of the S3 bucket.
        :param json_data: JSON object or dictionary to upload.
        :param s3_key: S3 key (path) where the file will be stored.
        """
        try:
            json_string = json.dumps(json_data)
            self.s3_client.put_object(Body=json_string, Bucket=bucket_name, Key=s3_key, ContentType='application/json')
            print(f"JSON file uploaded successfully to {bucket_name}/{s3_key}")
        except Exception as e:
            print(f"An error occurred while uploading the JSON file: {e}")