import boto3
from botocore.config import Config
from fastapi import UploadFile
from io import BytesIO

from app.core import Settings

class MinIOConnect:
    s3 = boto3.client(
        "s3",
        endpoint_url=Settings.MINIO_ENDPOINT,
        aws_access_key_id=Settings.MINIO_ACCESS_KEY,
        aws_secret_access_key=Settings.MINIO_SECRET_KEY,
        config=Config(
            connect_timeout=300,
            max_pool_connections=5,
            retries={
                'max_attempts': 10,
                'mode': 'standard'
            }
        )
    )

    @classmethod
    def ensure_bucket(cls): 
        buckets = cls.s3.list_buckets()['Buckets']
        if not any(b['Name'] == Settings.MINIO_BUCKET_NAME for b in buckets):
            cls.s3.create_bucket(Bucket=Settings.MINIO_BUCKET_NAME)

    @classmethod
    def ensure_folder(cls):
        cls.s3.put_object(Bucket=Settings.MINIO_BUCKET_NAME, Key=Settings.MINIO_FOLDER_DATA)

    @classmethod
    async def upload_file(cls, file: UploadFile, file_name: str):
        cls.s3.upload_fileobj(file.file, Settings.MINIO_BUCKET_NAME, f'{Settings.MINIO_FOLDER_DATA}{file_name}')

    @classmethod
    def delete_file(cls, file_name: str):
        cls.s3.delete_object(Bucket=Settings.MINIO_BUCKET_NAME, Key=f'{Settings.MINIO_FOLDER_DATA}{file_name}')

    @classmethod
    def download_file(cls, file_name: str):
        res = cls.s3.get_object(Bucket=Settings.MINIO_BUCKET_NAME, Key=f'{Settings.MINIO_FOLDER_DATA}{file_name}')
        return res['Body']
    
    @classmethod
    def upload_read_file(cls, content: str, file_name: str):
        cls.s3.put_object(Bucket=Settings.MINIO_BUCKET_NAME, Key=Settings.MINIO_FOLDER_STOR)
        byte_io = BytesIO(content.encode('utf-8'))
        cls.s3.upload_fileobj(byte_io, Settings.MINIO_BUCKET_NAME, f'{Settings.MINIO_FOLDER_STOR}/{file_name}')
        
    @classmethod
    def download_read_file(cls, file_name: str):
        res = cls.s3.get_object(Bucket=Settings.MINIO_BUCKET_NAME, Key=f'{Settings.MINIO_FOLDER_STOR}/{file_name}')
        return res['Body']
