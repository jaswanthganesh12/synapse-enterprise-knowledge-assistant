from sqlalchemy.orm import Session

from app.models.document import Document


def create_document(
    db: Session,
    title: str,
    original_filename: str,
    stored_filename: str,
    file_path: str,
    mime_type: str,
    source_type: str,
    uploaded_by: int,
) -> Document:

    document = Document(
        title=title,
        original_filename=original_filename,
        stored_filename=stored_filename,
        file_path=file_path,
        mime_type=mime_type,
        source_type=source_type,
        uploaded_by=uploaded_by,
        status="UPLOADED",
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document

def update_document_file(
    db: Session,
    document: Document,
    original_filename: str,
    stored_filename: str,
    file_path: str,
) -> Document:

    document.original_filename = original_filename
    document.stored_filename = stored_filename
    document.file_path = file_path

    db.commit()
    db.refresh(document)

    return document