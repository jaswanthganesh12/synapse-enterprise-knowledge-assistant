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
):

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