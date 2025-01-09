import boto3

class S3Manager:
    def __init__(self, region_name):
        """
        Initialize the S3 client.

        :param region_name: AWS region where the bucket is located.
        """
        self.s3_client = boto3.client('s3', region_name=region_name)

    def upload_text_file(self, bucket_name, s3_key, content):
        """
        Upload a single text file to an S3 bucket.

        :param bucket_name: Name of the S3 bucket.
        :param s3_key: S3 key (path) where the file will be stored.
        :param content: Content of the file to be uploaded.
        :return: True if upload is successful, False otherwise.
        """
        try:
            # Upload file content to S3
            self.s3_client.put_object(
                Body=content,
                Bucket=bucket_name,
                Key=s3_key,
                ContentType='text/plain'
            )
            print(f"File uploaded successfully to {bucket_name}/{s3_key}")
            return True
        except Exception as e:
            print(f"Failed to upload {s3_key} to {bucket_name}: {e}")
            return False