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
        
        
def create_flashcards_usecase(db: db_dependency, flashcards_list: FlashcardsListRequest, user_id: str) -> List[dict]:
    flashcards = [Flashcards(
        **flashcard.model_dump(), 
        user_id=user_id
    ) for flashcard in flashcards_list.data]

    result = []

    for flashcard in flashcards:
        db.add(flashcard)
        db.commit()
        db.refresh(flashcard)
        result.append(flashcard.to_dict())

    return result

def retrieve_all_flashcards_usecase(db: db_dependency, topic_id: str, user_id: str, page: int = 1, limit: int = 10) -> Dict[str, any]:
    offset = (page - 1) * limit

    flashcards_query = db.query(Flashcards).filter(
        Flashcards.topic_id == topic_id,
        Flashcards.user_id == user_id,
        Flashcards.deleted_at == None
    )

    total_flashcards = flashcards_query.count()
    flashcards = flashcards_query.offset(offset).limit(limit).all()

    result = {
        'total': total_flashcards,
        'page': page,
        'limit': limit,
        'flashcards': flashcards
    }
    
    return result

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