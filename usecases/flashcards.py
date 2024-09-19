from typing import List

from models.flashcard_model import Flashcards
from models.requests_model import FlashcardsListRequest
from utils import token_counter
from core.openai import client as openai_client
from database import db_dependency


def generate_flashcards_usecase(content: str, quantity: int) -> List[dict]:
    generated_flashcards = []
    
    if token_counter(content) > 1.6e4:
        content_slices = []
        #TODO: Adiciona slices
        for piece in content_slices:
            flashcards_list = openai_client.flash_card_generator(prompt=piece,\
                history=generated_flashcards, quantity=quantity)
            generated_flashcards.extend(flashcards_list)
    else:
        generated_flashcards = openai_client.flash_card_generator(prompt=content,\
            history=generated_flashcards, quantity=quantity)
        
    return generated_flashcards
        
        
def create_flashcards_usecase(db: db_dependency, flashcards_list: FlashcardsListRequest, user_id: str) -> List[dict]:
    flashcards = [Flashcards(**flashcard.model_dump(), user_id=user_id) for flashcard in flashcards_list.data]

    result = []

    for flashcard in flashcards:
        db.add(flashcard)
        db.commit()
        db.refresh(flashcard)
        result.append(flashcard)

    return result

def retrieve_all_flashcards_usecase(db: db_dependency, subject_id: str, user_id: str) -> List[dict]:
    result = db.query(Flashcards).filter(Flashcards.subject_id == subject_id,
        Flashcards.user_id == user_id, Flashcards.deleted_at == None).all()
    return result