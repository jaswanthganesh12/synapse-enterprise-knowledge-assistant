from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk


def create_chunks(
    db: Session,
    document_id: int,
    chunks: list,
) -> list[DocumentChunk]:

    db_chunks = [
        DocumentChunk(
            document_id=document_id,
            chunk_index=chunk.chunk_index,
            text=chunk.text,
            page_number=chunk.metadata.get("page_number"),
        )
        for chunk in chunks
    ]

    db.add_all(db_chunks)
    db.commit()

    for db_chunk in db_chunks:
        db.refresh(db_chunk)

    return db_chunks