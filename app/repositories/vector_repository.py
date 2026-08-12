from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

from app.core.config import settings


def upsert_vectors(
    client: QdrantClient,
    points: list[PointStruct],
) -> None:

    client.upsert(
        collection_name=settings.qdrant_collection,
        points=points,
    )