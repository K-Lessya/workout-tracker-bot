import boto3
from app.config import PHOTO_BUCKET
from botocore.exceptions import ClientError
import logging

def upload_file(file, destination):
    client = boto3.client('s3')
    try:
        response = client.upload_file(file, PHOTO_BUCKET, destination)
    except ClientError as e:
        logging.error(e)
        return False
    return True
