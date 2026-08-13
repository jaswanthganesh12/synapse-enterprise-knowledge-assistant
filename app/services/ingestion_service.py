from app.chunking.text_chunker import chunk_document
from app.core.enums import DocumentStatus
from app.db.session import SessionLocal
from app.models.document import Document
from app.repositories.document_chunk_repository import create_chunks
from app.parsers.registry import PARSER_REGISTRY


def process_document(document_id: int) -> None:
    db = SessionLocal()

    try:
        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if not document:
            return

        document.status = DocumentStatus.PROCESSING
        db.commit()

        parser = PARSER_REGISTRY.get(
            document.source_type
        )

        if not parser:
            raise ValueError(
                f"Unsupported source type: {document.source_type}"
            )

        parsed_document = parser(
            document.file_path
)

        chunks = chunk_document(
            parsed_document
        )

        if not chunks:
            raise ValueError(
                "No text could be extracted from document"
            )

        create_chunks(
            db=db,
            document_id=document.id,
            chunks=chunks,
        )

        document.status = DocumentStatus.INDEXED
        db.commit()

    except Exception:
        db.rollback()

        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if document:
            document.status = DocumentStatus.FAILED
            db.commit()

        raise

    finally:
        db.close()