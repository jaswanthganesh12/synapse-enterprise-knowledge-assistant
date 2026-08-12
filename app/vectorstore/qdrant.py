from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.core.config import settings


qdrant_client = QdrantClient(
    url=settings.qdrant_url,
)


def create_collection_if_not_exists() -> None:
    collections = qdrant_client.get_collections().collections

    existing_names = {
        collection.name
        for collection in collections
    }

    if settings.qdrant_collection in existing_names:
        return

    qdrant_client.create_collection(
        collection_name=settings.qdrant_collection,
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE,
        ),
    )
