from datetime import datetime
from typing import Annotated, List, Optional
from pydantic import BaseModel
from starlette import status
from models.flashcard_model import Flashcards
from usecases.auth import get_current_user_usecase

from utils import constants, pdf_to_text
from database import db_dependency

from fastapi import APIRouter, Depends, HTTPException, Path, UploadFile


router = APIRouter(
    prefix='/flashcards',
    tags=['flashcards']
)

user_dependency = Annotated[dict, Depends(get_current_user_usecase)]

class FlashcardRequest(BaseModel):
    subject_id: int
    topic_id: int
    question: str
    answer: str
    difficulty: int
    image_url: Optional[str] = None

class FlashcardsList(BaseModel):
    data: List[FlashcardRequest]

@router.post("/generate", status_code=status.HTTP_201_CREATED)
async def generate_flashcards(file: UploadFile, quantity: int = 5):
    try:
        text_content = pdf_to_text(pdf=file.file)
        #flashcards_list = generate_flashcards_usecase(content=text_content, quantity=quantity)
        flashcards_list = constants.FLASHCARDS_RESPONSE_MOCK
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro durante a conversão do PDF: {str(e)}")

    return {"flashcards": flashcards_list}

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_flashcards(db: db_dependency, user: user_dependency, flashcard_list: FlashcardsList):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')

    flashcards = [Flashcards(**flashcard.model_dump(), user_id=user.get('id')) for flashcard in flashcard_list.data]

    for flashcard in flashcards:
        db.add(flashcard)
        db.commit()

@router.get("/")
async def retrieve_all_flashcards(user: user_dependency, db: db_dependency):
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='authentication failed')
    return db.query(Flashcards).filter(
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