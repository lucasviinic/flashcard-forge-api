from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path, Query
from starlette import status

from database import db_dependency

from models.requests_model import SessionFlashcardRequest, SessionRequest
from usecases.auth import get_current_user_usecase
from usecases.sessions import create_session_usecase, retrieve_sessions_usecase


router = APIRouter(
    prefix='/sessions',
    tags=['sessions']
)

user_dependency = Annotated[dict, Depends(get_current_user_usecase)]

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_session(db: db_dependency, user: user_dependency, session_request: SessionRequest):
    try:
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
        response = create_session_usecase(db, session_request)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"error creating database session: {str(e)}")
    
    return response

@router.get("", status_code=status.HTTP_200_OK)
async def retrieve_all_sessions(
    db: db_dependency, 
    user: user_dependency,
    limit: int = Query(default=20, ge=1),
    offset: int = Query(default=0, ge=0),
    search: str = Query(default=None)
):
    try:
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
        sessions_list = retrieve_sessions_usecase(db, limit, offset, search)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"error getting sessions: {str(e)}")
    
    return sessions_list