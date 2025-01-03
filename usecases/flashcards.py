from datetime import datetime, timezone
import os
from typing import Dict, List, Optional

from fastapi import HTTPException
from sqlalchemy import func

from models.flashcard_model import Flashcards
from models.requests_model import FlashcardRequest, FlashcardsListRequest
from utils import token_counter
from core.openai import client as openai_client
from database import db_dependency
from utils.utils import fragment_text


def generate_flashcards_usecase(db: db_dependency, content: str, quantity: int, user_id: str, subject_id: str,
        topic_id: str, difficulty: int = 1) -> List[dict]:

    generated_flashcards = []
    text_fragments = fragment_text(content)

    for fragment in text_fragments:
        flashcards_list = openai_client.flash_card_generator(prompt=fragment,\
            history=generated_flashcards, quantity=quantity, difficulty=difficulty)
        generated_flashcards.extend(flashcards_list)

    result = []

    for flashcard in generated_flashcards:
        flashcard_model = Flashcards()

        flashcard_model.question = flashcard.get('question')
        flashcard_model.answer = flashcard.get('answer')

        flashcard_model.user_id = user_id
        flashcard_model.subject_id = subject_id
        flashcard_model.topic_id = topic_id
        flashcard_model.difficulty = difficulty
        flashcard_model.opened = False

        db.add(flashcard_model)
        db.commit()
        db.refresh(flashcard_model)

        result.append(flashcard_model.to_dict())
        
    return result
        
        
def create_flashcard_usecase(db: db_dependency, flashcard_request: FlashcardRequest, user_id: str) -> dict:
    flashcard_model = Flashcards(**flashcard_request.model_dump())
    flashcard_model.user_id = user_id

    db.add(flashcard_model)
    db.commit()
    db.refresh(flashcard_model)

    result = flashcard_model.to_dict()

    return result

def retrieve_all_flashcards_usecase(
        db: db_dependency,
        topic_id: str,
        user_id: str,
        limit: Optional[int] = 20,
        offset: Optional[int] = 0
    ) -> List[dict]:
    
    query = db.query(Flashcards).filter(
        Flashcards.topic_id == topic_id,
        Flashcards.user_id == user_id,
        Flashcards.deleted_at.is_(None)
    )

    if limit is None and offset is None:
        query = query.order_by(func.random())
    else:
        if limit is not None:
            query = query.limit(limit)
        if offset is not None:
            query = query.offset(offset)
    
    flashcards = query.all()
    return [flashcard.to_dict() for flashcard in flashcards]

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

def update_flashcard_usecase(db: db_dependency, user_id: str, flashcard_id: int, flashcard_request: FlashcardRequest) -> dict:
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
    flashcard_model.opened = flashcard_request.opened
    flashcard_model.updated_at = datetime.now(timezone.utc)

    db.add(flashcard_model)
    db.commit()

    result = flashcard_model.to_dict()

    return result