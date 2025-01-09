import boto3
import json
import os

class S3Manager:
    def __init__(self, region_name):
        self.s3_client = boto3.client('s3', region_name=region_name)

    def download_txt_files(self, bucket_name, local_folder):
        """
        Downloads all .txt files from a specified S3 bucket to a local folder.
        
        :param bucket_name: Name of the S3 bucket.
        :param local_folder: Local folder to save the downloaded .txt files.
        :return: List of downloaded file paths.
        """
        try:
            objects = self._list_files(bucket_name)

            if not objects:
                print("No files found in the bucket.")
                return []

            downloaded_files = []
            for file_key in objects:
                if file_key.endswith('.txt'):
                    local_path = os.path.join(local_folder, os.path.basename(file_key))
                    self.s3_client.download_file(bucket_name, file_key, local_path)
                    downloaded_files.append(local_path)

            return downloaded_files
        
        except Exception as e:
            print(f"An error occurred while downloading files: {e}")
            return []


    def _list_files(self, bucket_name):
        """
        List all files in the S3 bucket.

        :return: List of file keys in the bucket.
        """
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name)
            if 'Contents' in response:
                return [file['Key'] for file in response['Contents']]
            else:
                return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return None


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