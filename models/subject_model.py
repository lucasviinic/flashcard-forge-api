from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, func


class Subjects(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True, index=True)
    subject_name = Column(String, nullable=False)
    image_url = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)