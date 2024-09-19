from typing import List

from models.session_flashcards_model import SessionFlashcards
from models.session_model import SessionFlashcardRequest, Sessions
from database import db_dependency
from models.subject_model import Subjects
from models.topic_model import Topics 

def retrieve_all_subjects_usecase(db: db_dependency, user_id: str, limit: int = 10, offset: int = 0) -> List[dict]:
    subjects = db.query(Subjects).filter(Subjects.user_id == user_id)\
        .filter(Subjects.deleted_at == None).offset(offset).limit(limit).all()
    
    result = []
    
    for subject in subjects:
        topics = db.query(Topics).filter(Topics.subject_id == subject.id).all()
        topics_list = [topic.to_dict() for topic in topics]
        
        result.append({
            "id": subject.id,
            "user_id": subject.user_id,
            "updated_at": subject.updated_at,
            "created_at": subject.created_at,
            "subject_name": subject.subject_name,
            "image_url": subject.image_url,
            "deleted_at": subject.deleted_at,
            "topics": topics_list
        })
    
    return result