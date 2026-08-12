from qdrant_client.models import PointStruct
from sqlalchemy.orm import Session

from app.ai.embeddings import embed_texts
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.repositories.vector_repository import upsert_vectors
from app.vectorstore.qdrant import qdrant_client


def index_document_chunks(
    db: Session,
    document_id: int,
) -> None:

    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if not document:
        raise ValueError(
            f"Document {document_id} not found"
        )

    chunks = (
        db.query(DocumentChunk)
        .filter(
            DocumentChunk.document_id == document_id
        )
        .order_by(DocumentChunk.chunk_index)
        .all()
    )

    if not chunks:
        return

    texts = [
        chunk.text
        for chunk in chunks
    ]

    vectors = embed_texts(texts)

    points = []

    for chunk, vector in zip(chunks, vectors):
        points.append(
            PointStruct(
                id=chunk.id,
                vector=vector,
                payload={
                    "document_id": chunk.document_id,
                    "chunk_id": chunk.id,
                    "chunk_index": chunk.chunk_index,
                    "page_number": chunk.page_number,
                    "user_id": document.uploaded_by,
                    "filename": document.original_filename,
                    "source_type": document.source_type,
                },
            )
        )

    upsert_vectors(
        client=qdrant_client,
        points=points,
    )