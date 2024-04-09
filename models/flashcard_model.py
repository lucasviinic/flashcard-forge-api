from database import Base
from sqlalchemy import Column, ForeignKey, Boolean, Integer, String, DateTime, func


class Flashcards(Base):
    __tablename__ = 'flashcards'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    topic_id = Column(Integer, ForeignKey('topics.id'))
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    difficulty = Column(Integer, nullable=False)
    last_response = Column(Boolean, default=None)
    image_url = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)