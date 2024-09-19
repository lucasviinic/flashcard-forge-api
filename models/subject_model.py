import uuid

from pydantic import BaseModel, Field
from database import Base
from sqlalchemy import UUID, Column, ForeignKey, Integer, String, DateTime, func, inspect


class Subjects(Base):
    __tablename__ = 'subjects'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    subject_name = Column(String, nullable=False)
    image_url = Column(String)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    deleted_at = Column(DateTime)

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
    
class SubjectRequest(BaseModel):
    subject_name: str = Field(min_length=3, max_length=30)