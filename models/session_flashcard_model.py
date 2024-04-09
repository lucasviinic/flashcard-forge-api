from database import Base
from sqlalchemy import Column, DateTime, ForeignKey, Boolean, Integer, Interval, String, func


class SessionFlashcard(Base):
    __tablename__ = 'session_flashcard'

    id = Column(Integer, primary_key=True, index=True, comment="Unique identifier")
    session_id = Column(Integer, ForeignKey('sessions.id'), comment="Reference to session record ID")
    flashcard_id = Column(Integer, ForeignKey('flashcards.id'), comment="Reference to flashcard record ID"),
    response = Column(Boolean, nullable=False, comment="Answer given (correct or not)")
    difficulty = Column(Integer, nullable=False, comment="Flashcard difficulty, which can be 0, 1 or 2")
    created_at = Column(DateTime, default=func.now(), comment="Record creation date")
    updated_at = Column(DateTime, comment="Record update date")
    deleted_at = Column(DateTime, comment="Record deletion date")
