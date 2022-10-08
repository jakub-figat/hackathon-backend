import asyncio
import io
import os
from functools import partial
from uuid import UUID

import boto3
from fastapi import UploadFile

from src.settings import settings


s3_client = boto3.client("s3")


async def save_image_locally(image_uuid: UUID, image_file: UploadFile) -> str:
    file_path = f"/var/www/media/{str(image_uuid)}.jpg"
    with open(file_path, "wb") as file:
        file.write(await image_file.read())

    return file_path


async def upload_image_to_s3(image_uuid: UUID, image_file: UploadFile) -> str:
    file = io.BytesIO(await image_file.read())
    file_path = f"{str(image_uuid)}.jpg"
    upload_file_function = partial(
        s3_client.upload_fileobj,
        Fileobj=file,
        Bucket=settings.bucket_name,
        Key=file_path,
        ExtraArgs={"ContentType": "image/jpg"},
    )
    await asyncio.get_event_loop().run_in_executor(None, upload_file_function)

    return f"https://{settings.bucket_name}.s3.amazonaws.com/{file_path}"


async def remove_file_from_s3(file_path: str) -> None:
    s3_object_delete = partial(s3_client.delete_object, Bucket=settings.bucket_name, Key=file_path)
    await asyncio.get_event_loop().run_in_executor(None, s3_object_delete)


async def remove_file_locally(file_path: str) -> None:
    if os.path.exists(file_path):
        await asyncio.get_event_loop().run_in_executor(None, os.remove, file_path)
