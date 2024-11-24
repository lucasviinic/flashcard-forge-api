from datetime import datetime
from typing import Annotated, List
from starlette import status
from models.flashcard_model import Flashcards
from models.requests_model import FlashcardRequest, FlashcardsListRequest
from usecases.auth import get_current_user_usecase

from usecases.flashcards import create_flashcard_usecase, delete_flashcard_usecase, generate_flashcards_usecase, retrieve_all_flashcards_usecase, update_flashcard_usecase
from utils import constants, pdf_to_text
from database import db_dependency

from fastapi import APIRouter, Depends, HTTPException, Path, Query, UploadFile


router = APIRouter(
    prefix='/flashcards',
    tags=['flashcards']
)

user_dependency = Annotated[dict, Depends(get_current_user_usecase)]

@router.post("/generate", status_code=status.HTTP_201_CREATED)
async def generate_flashcards(file: UploadFile, quantity: int = Query(5, ge=1, le=10), difficulty: int = Query(1, ge=0, le=2)):
    try:
        text_content = pdf_to_text(pdf=file.file)
        flashcards_list = generate_flashcards_usecase(content=text_content, quantity=quantity, difficulty=difficulty)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro durante a conversão do PDF: {str(e)}")

    return {"flashcards": flashcards_list}

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_flashcards(db: db_dependency, user: user_dependency, flashcard_request: FlashcardRequest):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')

    try:
        flashcard_created = create_flashcard_usecase(db, flashcard_request, user_id=user.get('id'))
        response = flashcard_created
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error creating flashcards: {str(e)}")

    return response

@router.get("")
async def retrieve_all_flashcards(
    user: user_dependency,
    db: db_dependency,
    topic_id: str = Query(...),
    limit: int = Query(default=15, ge=1),
    offset: int = Query(default=0, ge=0)
):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    
    try:
        response = retrieve_all_flashcards_usecase(
            db, topic_id=topic_id, user_id=user.get('id'), limit=limit, offset=offset)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error listing flashcards: {str(e)}")

    return response

@router.delete("/{flashcard_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_flashcard(user: user_dependency, db: db_dependency, flashcard_id: str):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    
    try:
        delete_flashcard_usecase(db, user.get('id'), flashcard_id)
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error deleting flashcard: {str(e.detail)}")

    return None

@router.put("/{flashcard_id}", status_code=status.HTTP_200_OK)
async def update_flashcard(user: user_dependency, db: db_dependency, flashcard_request: FlashcardRequest, flashcard_id: str):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')

    try:
        update_flashcard_usecase(db, user.get('id'), flashcard_id, flashcard_request)
    except HTTPException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error updating flashcard: {str(e.detail)}")

    return {"detail": "Flashcard updated successfully"}