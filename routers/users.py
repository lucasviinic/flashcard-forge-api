from typing import Annotated
from starlette import status
from usecases.auth import get_current_user_usecase

from usecases.flashcards import create_flashcard_usecase, delete_flashcard_usecase, generate_flashcards_usecase, retrieve_all_flashcards_usecase, update_flashcard_usecase
from database import db_dependency

from fastapi import APIRouter, Depends, HTTPException

from usecases.user import retrieve_user_usecase


router = APIRouter(
    prefix='/users',
    tags=['users']
)

user_dependency = Annotated[dict, Depends(get_current_user_usecase)]

@router.get("")
async def retrieve_user(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')

    try:
        user_data = retrieve_user_usecase(db=db_dependency, user_id=user.get('id'))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"error getting user: {str(e)}")

    return user_data