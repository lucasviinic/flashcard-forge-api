from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func


class Topics(Base):
    __tablename__ = 'topics'

    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    image_url = Column(String)
    topic_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)