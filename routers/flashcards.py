from datetime import datetime
from typing import Annotated, List
from starlette import status
from models.flashcard_model import Flashcards
from models.requests_model import FlashcardRequest, FlashcardsListRequest
from usecases.auth import get_current_user_usecase

from usecases.flashcards import create_flashcards_usecase, generate_flashcards_usecase
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

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_flashcards(db: db_dependency, user: user_dependency, flashcards_list: FlashcardsListRequest):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')

    response = create_flashcards_usecase(db, flashcards_list, user_id=user.get('id'))

    return response

@router.get("/")
async def retrieve_all_flashcards(user: user_dependency, db: db_dependency, topic_id: str = Query(...)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    return db.query(Flashcards).filter(Flashcards.topic_id == topic_id,
        Flashcards.user_id == user.get('id'), Flashcards.deleted_at == None).all()

@router.delete("/{flashcard_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_flashcard(user: user_dependency, db: db_dependency, flashcard_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    
    flashcard_model = db.query(Flashcards).filter(Flashcards.id == flashcard_id)\
        .filter(Flashcards.user_id == user.get('id')).first()
    
    if not flashcard_model:
        raise HTTPException(status_code=404, detail='flashcard not found')
    
    flashcard_model.deleted_at = datetime.now()
    
    db.add(flashcard_model)
    db.commit()

@router.put("/{flashcard_id}")
async def update_flashcard(user: user_dependency, db: db_dependency, flashcard_request: FlashcardRequest, flashcard_id: int = Path(gt=0)):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    
    flashcard_model = db.query(Flashcards).filter(Flashcards.id == flashcard_id)\
        .filter(Flashcards.user_id == user.get('id')).first()
    
    if not flashcard_model:
        raise HTTPException(status_code=404, detail='flashcard not found')
    
    flashcard_model.question = flashcard_request.question
    flashcard_model.answer = flashcard_request.answer
    flashcard_model.updated_at = datetime.now()

    db.add(flashcard_model)
    db.commit()