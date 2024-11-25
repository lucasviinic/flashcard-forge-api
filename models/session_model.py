import uuid
from database import Base
from sqlalchemy import UUID, Column, DateTime, ForeignKey, Integer, String, func


class Sessions(Base):
    __tablename__ = 'sessions'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4, comment="Unique identifier")
    subject_id = Column(String, nullable=False, comment="Subject ID")
    topic_id = Column(UUID(as_uuid=True), ForeignKey("topics.id"), comment="Reference to topic record ID")
    topic_name = Column(String, nullable=False, comment="Topic name")
    correct_answer_count = Column(Integer, nullable=False, comment="Number of correct answers")
    incorrect_answer_count = Column(Integer, nullable=False, comment="Number of incorrect answers")
    total_questions = Column(Integer, nullable=False, comment="Total number of questions")
    total_time_spent = Column(String, nullable=False, comment="Total time spent in the session")
    easy_question_count = Column(Integer, nullable=False, comment="Number of easy questions")
    medium_question_count = Column(Integer, nullable=False, comment="Number of medium questions")
    hard_question_count = Column(Integer, nullable=False, comment="Number of hard questions")
    created_at = Column(DateTime, default=func.now(), comment="Record creation date")
    updated_at = Column(DateTime, comment="Record update date")
    deleted_at = Column(DateTime, comment="Record deletion date")

    def to_dict(self):
        """
        Converts a SQLAlchemy object to a dictionary.
        """
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}