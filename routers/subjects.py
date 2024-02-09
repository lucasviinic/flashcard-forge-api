from typing import Annotated
from pydantic import BaseModel, Field
from starlette import status

from fastapi import APIRouter, Depends, HTTPException, Path

from models.subject_model import Subjects
from usecases.auth import get_current_user_usecase
from database import db_dependency


router = APIRouter(
    prefix='/subjects',
    tags=['subjects']
)

user_dependency = Annotated[dict, Depends(get_current_user_usecase)]

class SubjectRequest(BaseModel):
    subject_name: str = Field(min_length=3, max_length=30)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_subject(db: db_dependency, user: user_dependency, subject_request: SubjectRequest):    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    
    subject_model = Subjects(**subject_request.model_dump(), user_id=user.get('id'))

    db.add(subject_model)
    db.commit()

@router.get("/")
async def retrieve_all_subjects(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    
    return db.query(Subjects).filter(Subjects.user_id == user.get('id')).all()

@router.put("/{subject_id}")
async def update_subject(user: user_dependency, db: db_dependency, subject_request: SubjectRequest, subject_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    
    subject_model = db.query(Subjects).filter(Subjects.id == subject_id)\
        .filter(Subjects.user_id == user.get('id')).first()
    
    if not subject_model:
        raise HTTPException(status_code=404, detail='subject not found')
    
    subject_model.subject_name = subject_request.subject_name

    db.add(subject_model)
    db.commit()

@router.get("/{subject_id}", status_code=status.HTTP_200_OK)
async def retrieve_subject(user: user_dependency, db: db_dependency, subject_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    
    subject_model = db.query(Subjects).filter(Subjects.id == subject_id)\
        .filter(Subjects.user_id == user.get('id')).first()

    if not subject_model:
        raise HTTPException(status_code=404, detail='subject not found')
    
    return subject_model
    
@router.delete("/{subject_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_subject(user: user_dependency, db: db_dependency, subject_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    
    subject_model = db.query(Subjects).filter(Subjects.id == subject_id)\
        .filter(Subjects.user_id == user.get('id')).first()
    
    if not subject_model:
        raise HTTPException(status_code=404, detail='subject not found')
    
    db.query(Subjects).filter(Subjects.id == subject_id).filter(Subjects.user_id == user.get('id')).delete()
    db.commit()