from datetime import datetime, timezone
import os
from typing import Dict, List

from fastapi import HTTPException

from models.flashcard_model import Flashcards
from models.requests_model import FlashcardRequest, FlashcardsListRequest
from utils import token_counter
from core.openai import client as openai_client
from database import db_dependency
from utils.utils import fragment_text


def generate_flashcards_usecase(content: str, quantity: int, difficulty: int = 1) -> List[dict]:
    generated_flashcards = []
    text_fragments = fragment_text(content)

    for fragment in text_fragments:
        flashcards_list = openai_client.flash_card_generator(prompt=fragment,\
            history=generated_flashcards, quantity=quantity, difficulty=difficulty)
        generated_flashcards.extend(flashcards_list)
        
    return generated_flashcards
        
        
def create_flashcard_usecase(db: db_dependency, flashcard_request: FlashcardRequest, user_id: str) -> dict:
    flashcard_model = Flashcards(**flashcard_request.model_dump())
    flashcard_model.user_id = user_id

    db.add(flashcard_model)
    db.commit()
    db.refresh(flashcard_model)

    result = flashcard_model.to_dict()

    return result

def retrieve_all_flashcards_usecase(db: db_dependency, topic_id: str, user_id: str, limit: int = 20, offset: int = 0) -> List[dict]:
    flashcards_query = db.query(Flashcards).filter(
        Flashcards.topic_id == topic_id,
        Flashcards.user_id == user_id,
        Flashcards.deleted_at == None
    )

    flashcards = flashcards_query.offset(offset).limit(limit).all()
    
    return flashcards

def delete_flashcard_usecase(db: db_dependency, user_id: str, flashcard_id: int) -> None:
    flashcard_model = db.query(Flashcards).filter(
        Flashcards.id == flashcard_id,
        Flashcards.user_id == user_id
    ).first()

    if not flashcard_model:
        raise HTTPException(status_code=404, detail='Flashcard not found')

    flashcard_model.deleted_at = datetime.now(timezone.utc)

    db.add(flashcard_model)
    db.commit()

def update_flashcard_usecase(db: db_dependency, user_id: str, flashcard_id: int, flashcard_request: FlashcardRequest) -> None:
    flashcard_model = db.query(Flashcards).filter(
        Flashcards.id == flashcard_id,
        Flashcards.user_id == user_id,
        Flashcards.deleted_at == None
    ).first()

    if not flashcard_model:
        raise HTTPException(status_code=404, detail='Flashcard not found')

    flashcard_model.question = flashcard_request.question
    flashcard_model.answer = flashcard_request.answer
    flashcard_model.difficulty = flashcard_request.difficulty
    flashcard_model.updated_at = datetime.now(timezone.utc)

    db.add(flashcard_model)
    db.commit()

    result = flashcard_model.to_dict()

    return result