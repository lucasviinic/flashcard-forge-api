import os
import dotenv
from fastapi import HTTPException

from database import db_dependency
from models.flashcard_model import Flashcards
from models.subject_model import Subjects
from models.topic_model import Topics
from models.user_model import Users


dotenv.load_dotenv()

def retrieve_user_usecase(db: db_dependency, user_id: str) -> dict:
    user_model = db.query(Users).filter(Users.id == user_id, Users.deleted_at.is_(None)).first()

    if not user_model:
        raise HTTPException(status_code=400, detail='user not found')

    flashcard_limit = os.getenv('DEFAULT_FLASHCARDS_LIMIT')
    flashcards_count = db.query(Flashcards).filter(Flashcards.user_id == user_id).count()
    flashcards_usage = f"{flashcards_count}/{flashcard_limit}"

    ai_gen_flashcards_limit = os.getenv('DEFAULT_AI_GEN_FLASHCARDS_LIMIT')
    ai_gen_flashcards_count = db.query(Flashcards).filter(
        Flashcards.user_id == user_id,
        Flashcards.origin == 'ai'
    ).count()
    ai_gen_flashcards_usage = f"{ai_gen_flashcards_count}/{ai_gen_flashcards_limit}"

    subjects_limit = os.getenv('DEFAULT_SUBJECTS_LIMIT')
    subjects_count = db.query(Subjects).filter(Subjects.user_id == user_id).count()
    subjects_usage = f"{subjects_count}/{subjects_limit}"

    if user_model.account_type == 1:
        flashcards_usage = "Unlimited"
        ai_gen_flashcards_usage = f"{ai_gen_flashcards_usage}/{os.getenv('PREMIUM_AI_GEN_FLASHCARDS_LIMIT')}"
        subjects_usage = "Unlimited"

    user_data = user_model.to_dict()

    user_data['flashcards_usage'] = flashcards_usage
    user_data['ai_gen_flashcards_usage'] = ai_gen_flashcards_usage
    user_data['subjects_usage'] = subjects_usage
    user_data['created_at'] = user_model.created_at.strftime('%B %d, %Y')

    return user_data
    
