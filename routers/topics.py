from typing import Annotated
from starlette import status

from fastapi import APIRouter, Depends, HTTPException, Query

from models.requests_model import TopicRequest
from usecases.auth import get_current_user_usecase
from database import db_dependency

from usecases.topics import create_topic_usecase, delete_topic_usecase, retrieve_all_topics_usecase, retrieve_topic_usecase, update_topic_usecase


router = APIRouter(
    prefix="/topics",
    tags=["topics"]
)

user_dependency = Annotated[dict, Depends(get_current_user_usecase)]

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_topic(db: db_dependency, user: user_dependency, topic_request: TopicRequest):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    
    response = create_topic_usecase(db, topic_request)

    return response

@router.get("/{subject_id}", status_code=status.HTTP_200_OK)
async def retrieve_all_topics(user: user_dependency, db: db_dependency, subject_id: str):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    
    response = retrieve_all_topics_usecase(db, subject_id)

    return response

@router.put("")
async def update_topic(user: user_dependency, db: db_dependency, topic_request: TopicRequest):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    
    response = update_topic_usecase(db, topic_request)
    
    return response

@router.get("/{subject_id}", status_code=status.HTTP_200_OK)
async def retrieve_topic(user: user_dependency, db: db_dependency, subject_id: str, topic_id: str = Query(...)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    
    response = retrieve_topic_usecase(db, subject_id, topic_id)

    return response

@router.delete("/{topic_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_topic(user: user_dependency, db: db_dependency, topic_id: str):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    
    delete_topic_usecase(db, topic_id)
