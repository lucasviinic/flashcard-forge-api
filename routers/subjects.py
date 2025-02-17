from datetime import datetime, timezone
import os
from typing import Annotated
from starlette import status

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

from models.requests_model import SubjectRequest
from models.subject_model import Subjects
from usecases.auth import get_current_user_usecase
from database import db_dependency
from usecases.subjects import create_subject_usecase, delete_subject_usecase, retrieve_all_subjects_usecase, retrieve_subject_usecase, update_subject_usecase

import firebase_admin
from firebase_admin import credentials, storage

from google.cloud.exceptions import NotFound


router = APIRouter(
    prefix='/subjects',
    tags=['subjects']
)

user_dependency = Annotated[dict, Depends(get_current_user_usecase)]

if not firebase_admin._apps:
    cred = credentials.Certificate("flashcardforge-firebase-adminsdk.json")
    firebase_admin.initialize_app(cred, {
        'storageBucket': f"{os.getenv('FIREBASE_PROJECT_ID')}.firebasestorage.app"
    })

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_subject(db: db_dependency, user: user_dependency, subject_request: SubjectRequest):    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    
    response = create_subject_usecase(db, subject_request, user_id=user.get('id'))

    return response

@router.get("")
async def retrieve_all_subjects(
    user: user_dependency,
    db: db_dependency,
    limit: int = Query(default=15, ge=1),
    offset: int = Query(default=0, ge=0),
    search: str = Query(default=None)
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    
    response = retrieve_all_subjects_usecase(db, user_id=user.get('id'), limit=limit, offset=offset, search=search)

    return response

@router.put("/{subject_id}")
async def update_subject(user: user_dependency, db: db_dependency, subject_request: SubjectRequest, subject_id: str):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    
    response = update_subject_usecase(db, subject_request, subject_id, user_id=user.get('id'))

    return response

@router.get("/{subject_id}", status_code=status.HTTP_200_OK)
async def retrieve_subject(user: user_dependency, db: db_dependency, subject_id: str):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    
    response = retrieve_subject_usecase(db, subject_id, user_id=user.get('id'))
    
    return response
    
@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subject(user: user_dependency, db: db_dependency, subject_id: str):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    
    delete_subject_usecase(db, subject_id, user_id=user.get('id'))

@router.put("/{subject_id}/upload-image", status_code=status.HTTP_200_OK)
async def update_subject_image(
    subject_id: str,
    user: user_dependency,
    db: db_dependency,
    file: UploadFile = File(...)
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')

    bucket = storage.bucket()
    blob = bucket.blob(f"subject-images/{subject_id}")

    try: blob.delete()
    except NotFound: pass

    try:
        blob.upload_from_file(file.file, content_type=file.content_type)
        blob.make_public()
        image_url = f"{blob.public_url}?v={datetime.now(timezone.utc).time()}"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao fazer upload da imagem para o Firebase: {str(e)}")

    subject_model = db.query(Subjects).filter(
        Subjects.id == subject_id,
        Subjects.user_id == user.get('id'),
        Subjects.deleted_at == None
    ).first()

    if not subject_model:
        raise HTTPException(status_code=404, detail='subject not found')
    
    subject_model.image_url = image_url
    subject_model.updated_at = datetime.now(timezone.utc)

    db.add(subject_model)
    db.commit()
    db.refresh(subject_model)

    return subject_model.to_dict()