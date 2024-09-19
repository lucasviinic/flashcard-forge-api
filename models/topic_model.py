import uuid
from database import Base
from sqlalchemy import UUID, Column, ForeignKey, String, DateTime, func, inspect


class Topics(Base):
    __tablename__ = 'topics'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id"))
    image_url = Column(String)
    topic_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now())
    deleted_at = Column(DateTime)

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}