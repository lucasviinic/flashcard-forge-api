import uuid
from database import Base
from sqlalchemy import UUID, CheckConstraint, Column, ForeignKey, Boolean, Integer, String, DateTime, func, inspect


class Flashcards(Base):
    __tablename__ = 'flashcards'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
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

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}