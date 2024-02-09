from typing import Annotated
from pydantic import BaseModel, Field
from starlette import status

from fastapi import APIRouter, Depends, HTTPException, Path

from models.topic_model import Topics
from usecases.auth import get_current_user_usecase
from database import db_dependency

from datetime import datetime


router = APIRouter(
    prefix="/topics",
    tags=["topics"]
)

user_dependency = Annotated[dict, Depends(get_current_user_usecase)]

class TopicRequest(BaseModel):
    topic_name: str = Field(min_length=3, max_length=30)
    subject_id: int

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_topic(db: db_dependency, user: user_dependency, topic_request: TopicRequest):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    
    topic_model = Topics(**topic_request.model_dump())

    db.add(topic_model)
    db.commit()

@router.get("/{subject_id}", status_code=status.HTTP_200_OK)
async def retrieve_all_topics(user: user_dependency, db: db_dependency, subject_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    
    return db.query(Topics).filter(Topics.subject_id == subject_id).all()

@router.put("/{topic_id}")
async def update_topic(user: user_dependency, db: db_dependency, topic_request: TopicRequest, topic_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    
    topic_model = db.query(Topics).filter(Topics.id == topic_id).first()

    if not topic_model:
        raise HTTPException(status_code=404, detail='topic not found')

    topic_model.topic_name = topic_request.topic_name
    topic_model.updated_at = datetime.now()
    
    db.add(topic_model)
    db.commit()

@router.get("/{topic_id}", status_code=status.HTTP_200_OK)
async def retrieve_topic(user: user_dependency, db: db_dependency, topic_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    
    topic_model = db.query(Topics).filter(Topics.id == topic_id).first()

    if not topic_model:
        raise HTTPException(status_code=404, detail='topic not found')
    
    return topic_model

@router.delete("/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_topic(user: user_dependency, db: db_dependency, topic_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    
    topic_model = db.query(Topics).filter(Topics.id == topic_id).first()

    if not topic_model:
        raise HTTPException(status_code=404, detail='topic not found')
    
    db.query(Topics).filter(Topics.id == topic_id).delete()
    db.commit()
