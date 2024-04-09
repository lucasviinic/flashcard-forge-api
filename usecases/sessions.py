from typing import List

from models.session_flashcard_model import SessionFlashcards
from models.session_model import SessionRequest, Sessions
from database import db_dependency as db


def create_session_usecase(session_request: SessionRequest) -> dict:
    session_model = Sessions(**session_request.model_dump())
    db.add(session_model)
    db.commit()

    db.refresh(session_model)
    session_id = session_model.id
    
    session_flashcards_models = []
    for flashcard in session_request.flashcards:
        session_flashcard = SessionFlashcards(**flashcard.model_dump(), session_id=session_id)
        session_flashcards_models.append(session_flashcard)
        db.add(session_flashcard)

    db.commit()

    session_data = session_model.dict()
    session_data["flashcards"] = [flashcard.dict() for flashcard in session_flashcards_models]

    return session_data

def retrieve_sessions_usecase(topic_id: int, limit: int = 10, offset: int = 0) -> List[dict]:
    sessions = db.query(Sessions).filter(Sessions.topic_id == topic_id).offset(offset).limit(limit).all()
    session_list = []

    for session in sessions:
        session_data = session.dict()
        session_flashcards = db.query(SessionFlashcards).filter(SessionFlashcards.session_id == session.id).all()
        session_data["flashcards"] = [flashcard.dict() for flashcard in session_flashcards]
        session_list.append(session_data)

    return session_list

