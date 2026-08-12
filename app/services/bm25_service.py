from rank_bm25 import BM25Okapi
from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk


def bm25_search(
    db: Session,
    query: str,
    user_id: int,
    limit: int = 5,
) -> list[tuple[DocumentChunk, float]]:

    chunks = (
        db.query(DocumentChunk)
        .join(
            Document,
            Document.id == DocumentChunk.document_id,
        )
        .filter(
            Document.uploaded_by == user_id
        )
        .order_by(
            DocumentChunk.document_id,
            DocumentChunk.chunk_index,
        )
        .all()
    )

    if not chunks:
        return []

    tokenized_chunks = [
        chunk.text.lower().split()
        for chunk in chunks
    ]

    bm25 = BM25Okapi(tokenized_chunks)

    query_tokens = query.lower().split()

    scores = bm25.get_scores(query_tokens)

    ranked = sorted(
        zip(chunks, scores),
        key=lambda item: item[1],
        reverse=True,
    )

    return ranked[:limit]