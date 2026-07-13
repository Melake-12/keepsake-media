import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.database import Base


def gen_uuid():
    return str(uuid.uuid4())


class Couple(Base):
    __tablename__ = "couples"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    name = Column(String, nullable=True)  # e.g. "Melake & ..."
    invite_code = Column(String, unique=True, index=True, default=lambda: uuid.uuid4().hex[:8])
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("User", back_populates="couple")


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    display_name = Column(String, nullable=False)
    couple_id = Column(UUID(as_uuid=False), ForeignKey("couples.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    couple = relationship("Couple", back_populates="users")


class Memory(Base):
    """A gallery item: one uploaded photo/video plus its caption/note."""
    __tablename__ = "memories"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    couple_id = Column(UUID(as_uuid=False), ForeignKey("couples.id"), nullable=False)
    uploaded_by = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    r2_object_key = Column(String, nullable=False)
    media_type = Column(String, default="image")  # image | video
    caption = Column(Text, nullable=True)
    taken_at = Column(DateTime, nullable=True)  # for "on this day" + timeline
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class JournalEntry(Base):
    __tablename__ = "journal_entries"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    couple_id = Column(UUID(as_uuid=False), ForeignKey("couples.id"), nullable=False)
    author_id = Column(UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    body = Column(Text, nullable=False)
    is_private = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class BucketListItem(Base):
    __tablename__ = "bucket_list_items"

    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    couple_id = Column(UUID(as_uuid=False), ForeignKey("couples.id"), nullable=False)
    title = Column(String, nullable=False)
    is_done = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
