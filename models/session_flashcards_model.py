import uuid
from database import Base
from sqlalchemy import UUID, Column, DateTime, ForeignKey, Boolean, Integer, Interval, String, func


class SessionFlashcards(Base):
    __tablename__ = 'session_flashcards'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4, comment="Unique identifier")
    session_id = Column(UUID(as_uuid=True), ForeignKey('sessions.id'), comment="Reference to session record ID")
    flashcard_id = Column(UUID(as_uuid=True), ForeignKey("flashcards.id"), comment="Reference to flashcard record ID")
    response = Column(Boolean, nullable=False, comment="Answer given (correct or not)")
    difficulty = Column(Integer, nullable=False, comment="Flashcard difficulty, which can be 0, 1 or 2")
    created_at = Column(DateTime, default=func.now(), comment="Record creation date")
    updated_at = Column(DateTime, comment="Record update date")
    deleted_at = Column(DateTime, comment="Record deletion date")

    def to_dict(self):
        """
        Converts a SQLAlchemy object to a dictionary.
        """
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
