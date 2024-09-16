import uuid
from database import Base
from sqlalchemy import UUID, Column, ForeignKey, Integer, String, DateTime, func


class Subjects(Base):
    __tablename__ = 'subjects'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    subject_name = Column(String, nullable=False)
    image_url = Column(String)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)