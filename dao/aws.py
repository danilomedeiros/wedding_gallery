from dotenv import load_dotenv
import os
import boto3

class Storage:

    def __init__(self):
        load_dotenv()
        self.bucket_name = os.environ.get('s3_bucket')
        print(self.bucket_name)
        self.resource = boto3.resource('s3')
        self.client = boto3.client('s3')
        self.bucket = self.resource.Bucket(self.bucket_name)


    def save(self, file_name, file_data):
        self.bucket.put_object(Key=file_name, Body=file_data)
        return 'true'

    def url(self, file_key):
        url = self.client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': self.bucket_name,
                'Key': file_key
            }
        )
        return url

