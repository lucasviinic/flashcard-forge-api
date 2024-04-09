from database import Base
from sqlalchemy import Column, DateTime, Integer, Interval, String, func


class Session(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True, index=True, comment="Unique identifier")
    score = Column(String, nullable=False, comment="User score, e.g. 7/20")
    time = Column(Interval, nullable=False, comment="Study session duration 00:09:31")
    easy = Column(Integer, nullable=False, comment="Number of easy flashcards")
    medium = Column(Integer, nullable=False, comment="Quantity of medium flashcards")
    hard = Column(Integer, nullable=False, comment="Quantity of hard flashcards")
    created_at = Column(DateTime, default=func.now(), comment="Record creation date")
    updated_at = Column(DateTime, comment="Record update date")
    deleted_at = Column(DateTime, comment="Record deletion date")