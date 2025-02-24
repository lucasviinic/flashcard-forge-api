from datetime import datetime
from typing import List, Optional, Dict
from fastapi import File, UploadFile
from pydantic import BaseModel, Field, validator


class TopicRequest(BaseModel):
    id: Optional[str] = Field(None)
    subject_id: str = Field(None)
    topic_name: str = Field(max_length=30)

class SubjectRequest(BaseModel):
    image_url: Optional[str] = None
    subject_name: str = Field(max_length=30)

class FlashcardRequest(BaseModel):
    flashcard_id: int
    response: bool
    difficulty: int

class SessionRequest(BaseModel):
    subject_id: str
    topic_id: str
    topic_name: str
    correct_answer_count: int
    incorrect_answer_count: int
    total_questions: int
    total_time_spent: str
    easy_question_count: int
    medium_question_count: int
    hard_question_count: int

class SessionFlashcardRequest(BaseModel):
    session: SessionRequest
    flashcards: Optional[List[FlashcardRequest]]

class FlashcardRequest(BaseModel):
    subject_id: str
    topic_id: str
    question: str
    answer: str
    difficulty: int
    opened: Optional[bool] = None
    image_url: Optional[str] = None

    @validator('difficulty')
    def check_difficulty(cls, value):
        if value not in {0, 1, 2}:
            raise ValueError('difficulty must be 0, 1, or 2')
        return value

class FlashcardsListRequest(BaseModel):
    data: List[FlashcardRequest]

class FeedbackRequest(BaseModel):
    feedback: str = Field(min_length=5, max_length=300)

class UserRequest(BaseModel):
    file_picture: UploadFile = File(...)


class ErrorLog(BaseModel):
    error_message: str = Field(..., description="Error description")
    stack_trace: str = Field(..., description="Stack trace detail")
    screen: Optional[str] = Field(None, description="Screen when error ocurred")
    timestamp: datetime = Field(..., description="Timestamp")
    device_info: Optional[Dict[str, str]] = Field(None, description="Device info")