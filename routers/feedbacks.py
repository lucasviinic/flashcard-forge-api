from typing import Annotated
from starlette import status
from models.requests_model import FeedbackRequest
from usecases.auth import get_current_user_usecase

from usecases.feedbacks import send_feedback_usecase
from database import db_dependency

from fastapi import APIRouter, Depends, HTTPException


router = APIRouter(
    prefix='/feedback',
    tags=['feedback']
)

user_dependency = Annotated[dict, Depends(get_current_user_usecase)]

@router.post("", status_code=status.HTTP_201_CREATED)
async def send_feedback(db: db_dependency, user: user_dependency, content: FeedbackRequest):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    
    try:
        send_feedback_usecase(db=db, user=user, content=content)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating flashcards: {str(e)}")

    return None