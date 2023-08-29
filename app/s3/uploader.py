import boto3
from app.config import PHOTO_BUCKET
from botocore.exceptions import ClientError
import logging
import asyncio
import os




async def update_progress(callback, percent):
    await callback.message.edit_text(f"Загрузка файла: {percent:.2f}%")

async def upload_to_s3_and_update_progress(loop,file_path, s3_file_key, callback):
    client = boto3.client('s3')
    total_size = os.path.getsize(file_path)

    def update_progress_callback(bytes_amount):
        percent = (bytes_amount / total_size) * 100
        asyncio.run_coroutine_threadsafe(update_progress(callback, percent), loop)

    client.upload_file(file_path, PHOTO_BUCKET, s3_file_key, Callback=update_progress_callback)
    await update_progress(callback=callback, percent=100.0)
    await callback.message.edit_text("Загрузка завершена!")





def upload_file(file, destination):
    client = boto3.client('s3')
    try:
        response = client.upload_file(file, PHOTO_BUCKET, destination)
    except ClientError as e:
        logging.error(e)
        return False
    return True



