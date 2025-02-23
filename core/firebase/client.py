import os
from datetime import datetime, timezone

from fastapi import UploadFile

import firebase_admin
from firebase_admin import credentials, storage
from google.cloud.exceptions import NotFound

from utils.utils import compress_image


def firebase_file_upload(bucket_blob: str, image_id: str, file_image: UploadFile) -> str:
    if not firebase_admin._apps:
        cred = credentials.Certificate("flashcardforge-firebase-adminsdk.json")
        firebase_admin.initialize_app(cred, {
            'storageBucket': f"{os.getenv('FIREBASE_PROJECT_ID')}.firebasestorage.app"
        })

    bucket = storage.bucket()
    blob = bucket.blob(f"{bucket_blob}/{image_id}")

    try:
        blob.delete()
    except NotFound:
        pass
    
    compressed_image = compress_image(file_image=file_image, quality=40)

    blob.upload_from_file(compressed_image, content_type=file_image.content_type)
    blob.make_public()

    image_url = f"{blob.public_url}?v={datetime.now(timezone.utc).time()}"

    return image_url
