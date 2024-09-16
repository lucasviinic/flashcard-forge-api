from typing import List
import uuid
from pydantic import BaseModel
from database import Base
from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, Interval, String, func


class Sessions(Base):
    __tablename__ = 'sessions'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4, comment="Unique identifier")
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id"), comment="Reference to topic record ID")
    score = Column(String, nullable=False, comment="User score, e.g. 7/20")
    time = Column(Interval, nullable=False, comment="Study session duration 00:09:31")
    easy = Column(Integer, nullable=False, comment="Number of easy flashcards")
    medium = Column(Integer, nullable=False, comment="Quantity of medium flashcards")
    hard = Column(Integer, nullable=False, comment="Quantity of hard flashcards")
    created_at = Column(DateTime, default=func.now(), comment="Record creation date")
    updated_at = Column(DateTime, comment="Record update date")
    deleted_at = Column(DateTime, comment="Record deletion date")

    def to_dict(self):
        """
        Converts a SQLAlchemy object to a dictionary.
        """
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class FlashcardRequest(BaseModel):
    flashcard_id: int
    response: bool
    difficulty: int

class SessionRequest(BaseModel):
    topic_id: int
    score: str
    time: str
    easy: int
    medium: int
    hard: int

class SessionFlashcardRequest(BaseModel):
    session: SessionRequest
    flashcards: List[FlashcardRequest]