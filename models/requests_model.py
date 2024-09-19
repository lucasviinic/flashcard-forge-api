from typing import List, Optional
from pydantic import BaseModel, Field


class TopicRequest(BaseModel):
    topic_name: str = Field(min_length=3, max_length=30)

class SubjectRequest(BaseModel):
    subject_name: str = Field(min_length=3, max_length=30)

class FlashcardRequest(BaseModel):
    flashcard_id: int
    response: bool
    difficulty: int

class SessionRequest(BaseModel):
    topic_id: str
    score: str
    time: str
    easy: int
    medium: int
    hard: int

class SessionFlashcardRequest(BaseModel):
    session: SessionRequest
    flashcards: List[FlashcardRequest]

class FlashcardRequest(BaseModel):
    subject_id: int
    topic_id: int
    question: str
    answer: str
    difficulty: int
    image_url: Optional[str] = None

class FlashcardsListRequest(BaseModel):
    data: List[FlashcardRequest]