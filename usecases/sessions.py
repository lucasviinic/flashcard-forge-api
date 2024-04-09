from typing import List

from models.session_flashcards_model import SessionFlashcards
from models.session_model import SessionFlashcardRequest, Sessions
from database import db_dependency


def create_session_usecase(db: db_dependency, session_request: SessionFlashcardRequest) -> dict:
    session_model = Sessions(**session_request.session.model_dump())
    db.add(session_model)
    db.commit()
    
    session_flashcards_models = []
    for flashcard in session_request.flashcards:
        session_flashcard = SessionFlashcards(**flashcard.model_dump(), session_id=session_model.id)
        session_flashcards_models.append(session_flashcard)
        db.add(session_flashcard)
    db.commit()

    session_data = session_model.to_dict()
    session_data["flashcards"] = [flashcard.to_dict() for flashcard in session_flashcards_models]

    return session_data

def retrieve_sessions_usecase(db: db_dependency, topic_id: int, limit: int = 10, offset: int = 0) -> List[dict]:
    sessions = db.query(Sessions).filter(Sessions.topic_id == topic_id).offset(offset).limit(limit).all()
    session_list = []

    for session in sessions:
        session_data = session.to_dict()
        session_flashcards = db.query(SessionFlashcards).filter(SessionFlashcards.session_id == session.id).all()
        session_data["flashcards"] = [flashcard.to_dict() for flashcard in session_flashcards]
        session_list.append(session_data)

    return session_list
