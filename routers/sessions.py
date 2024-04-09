from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status

from database import db_dependency

from models.session_model import SessionFlashcardRequest
from usecases.auth import get_current_user_usecase
from usecases.sessions import create_session_usecase, retrieve_sessions_usecase


router = APIRouter(
    prefix='/sessions',
    tags=['sessions']
)

user_dependency = Annotated[dict, Depends(get_current_user_usecase)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_session(db: db_dependency, user: user_dependency, session_request: SessionFlashcardRequest):
    try:
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
        session_data = create_session_usecase(db, session_request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"error creating database session: {str(e)}")
    
    return {"session": session_data}

@router.get("/{topic_id}", status_code=status.HTTP_200_OK)
async def retrieve_all_sessions(db: db_dependency, user: user_dependency, topic_id: int = Path(gt=0), limit: int = 10, offset: int = 0):
    try:
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
        sessions_list = retrieve_sessions_usecase(db, topic_id, limit, offset)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"error getting sessions: {str(e)}")
    
    return sessions_list