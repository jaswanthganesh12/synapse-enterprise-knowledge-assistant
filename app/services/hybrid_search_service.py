from sqlalchemy.orm import Session
from app.models.document_chunk import DocumentChunk
from app.ai.reranker import rerank
from app.services.bm25_service import bm25_search
from app.services.search_service import semantic_search


def hybrid_search(
    db: Session,
    query: str,
    user_id: int,
    limit: int = 5,
    candidate_limit: int = 10,
) -> list[dict]:

    vector_results = semantic_search(
        query=query,
        user_id=user_id,
        limit=candidate_limit,
    )

    bm25_results = bm25_search(
        db=db,
        query=query,
        user_id=user_id,
        limit=candidate_limit,
    )

    rrf_scores: dict[int, float] = {}
    chunk_data: dict[int, dict] = {}

    k = 60

    for rank, result in enumerate(
        vector_results,
        start=1,
    ):
        chunk_id = result.payload["chunk_id"]

        rrf_scores[chunk_id] = (
            rrf_scores.get(chunk_id, 0.0)
            + 1 / (k + rank)
        )

        chunk_data[chunk_id] = {
            "chunk_id": chunk_id,
            "document_id": result.payload["document_id"],
            "chunk_index": result.payload["chunk_index"],
            "page_number": result.payload["page_number"],
            "vector_score": result.score,
            "filename": result.payload.get("filename"),
            "source_type": result.payload.get("source_type"),
        }

    for rank, (chunk, score) in enumerate(
        bm25_results,
        start=1,
    ):
        chunk_id = chunk.id

        rrf_scores[chunk_id] = (
            rrf_scores.get(chunk_id, 0.0)
            + 1 / (k + rank)
        )

        if chunk_id not in chunk_data:
            chunk_data[chunk_id] = {
                "chunk_id": chunk_id,
                "document_id": chunk.document_id,
                "chunk_index": chunk.chunk_index,
                "page_number": chunk.page_number,
            }

        chunk_data[chunk_id]["bm25_score"] = score

    ranked = sorted(
        chunk_data.values(),
        key=lambda item: rrf_scores[item["chunk_id"]],
        reverse=True,
    )

    candidates = ranked[:candidate_limit]

    chunk_ids = [
        item["chunk_id"]
        for item in candidates
    ]

    db_chunks = (
    db.query(DocumentChunk)
    .filter(
        DocumentChunk.id.in_(chunk_ids)
    )
    .all()
)

    chunk_map = {
        chunk.id: chunk
        for chunk in db_chunks
    }

    documents = [
        chunk_map[item["chunk_id"]].text
        for item in candidates
        if item["chunk_id"] in chunk_map
    ]

    reranked_indices = rerank(
        query=query,
        documents=documents,
        top_k=limit,
    )

    final_results = []

    for new_rank, (index, score) in enumerate(
        reranked_indices,
        start=1,
    ):
        item = candidates[index].copy()

        item["rerank_score"] = float(score)
        item["rank"] = new_rank
        item["text"] = chunk_map[
            item["chunk_id"]
        ].text

        final_results.append(item)

    return final_results