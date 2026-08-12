from qdrant_client.models import FieldCondition, Filter, MatchValue, ScoredPoint

from app.ai.embeddings import embed_query
from app.core.config import settings
from app.vectorstore.qdrant import qdrant_client


def semantic_search(
    query: str,
    user_id: int,
    limit: int = 5,
) -> list[ScoredPoint]:

    query_vector = embed_query(query)

    user_filter = Filter(
        must=[
            FieldCondition(
                key="user_id",
                match=MatchValue(value=user_id),
            )
        ]
    )

    results = qdrant_client.query_points(
        collection_name=settings.qdrant_collection,
        query=query_vector,
        query_filter=user_filter,
        limit=limit,
        with_payload=True,
    )

    return results.points