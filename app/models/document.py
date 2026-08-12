from datetime import datetime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models.document_chunk import DocumentChunk

from sqlalchemy import (
    DateTime,
    ForeignKey,
    String,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.base import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String(255)
    )

    source_type: Mapped[str] = mapped_column(
        String(50)
    )

    file_path: Mapped[str] = mapped_column(
        String(500)
    )

    mime_type: Mapped[str] = mapped_column(
        String(100)
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="UPLOADED"
    )

    uploaded_by: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    owner = relationship(
    "User",
    back_populates="documents",
    )

    original_filename: Mapped[str] = mapped_column(
    String(255)
   )

    stored_filename: Mapped[str] = mapped_column(
    String(255)
   )

    chunks: Mapped[list["DocumentChunk"]] = relationship(
    back_populates="document",
    cascade="all, delete-orphan",
    )