from typing import List

from models.requests_model import SessionFlashcardRequest
from models.session_flashcards_model import SessionFlashcards
from models.session_model import Sessions
from database import db_dependency


def create_session_usecase(db: db_dependency, session_request: SessionFlashcardRequest,  user_id: str) -> dict:
    session_model = Sessions(**session_request.model_dump(), user_id=user_id)
    db.add(session_model)
    db.commit()
    
    # session_flashcards_models = []
    # for flashcard in session_request.flashcards:
    #     session_flashcard = SessionFlashcards(**flashcard.model_dump(), session_id=session_model.id)
    #     session_flashcards_models.append(session_flashcard)
    #     db.add(session_flashcard)
    # db.commit()

    session_data = session_model.to_dict()

    return session_data

def retrieve_sessions_usecase(db: db_dependency, user_id: str, limit: int, offset: int, search: str) -> List[dict]:
    query = db.query(Sessions).filter(Sessions.user_id == user_id).filter(Sessions.deleted_at == None)
    
    if search:
        query = query.filter(Sessions.topic_name.ilike(f"%{search}%"))

    sessions = query.offset(offset).limit(limit).all()
    result = [session.to_dict() for session in sessions]

    return result
