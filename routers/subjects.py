from typing import Annotated
from starlette import status

from fastapi import APIRouter, Depends, HTTPException, Query

from models.requests_model import SubjectRequest
from usecases.auth import get_current_user_usecase
from database import db_dependency
from usecases.subjects import create_subject_usecase, delete_subject_usecase, retrieve_all_subjects_usecase, retrieve_subject_usecase, update_subject_usecase


router = APIRouter(
    prefix='/subjects',
    tags=['subjects']
)

user_dependency = Annotated[dict, Depends(get_current_user_usecase)]

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
