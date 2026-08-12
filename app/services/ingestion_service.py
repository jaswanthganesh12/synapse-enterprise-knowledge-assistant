import time

from app.core.enums import DocumentStatus
from app.db.session import SessionLocal
from app.models.document import Document


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

        # Temporary processing simulation.
        # Real document parsing will replace this.
        time.sleep(2)

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