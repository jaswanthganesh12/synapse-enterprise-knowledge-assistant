import gc
import statistics
import time

from sentence_transformers import SentenceTransformer
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.vectorstore.qdrant import qdrant_client


MODEL_NAME = "all-MiniLM-L6-v2"
VECTOR_SIZE = 384

TEST_COLLECTION = "synapse_benchmark_10k"

DOCUMENT_COUNT = 10000
CHUNKS_PER_DOCUMENT = 3


def create_test_collection():
    existing = {
        collection.name
        for collection in qdrant_client.get_collections().collections
    }

    if TEST_COLLECTION in existing:
        qdrant_client.delete_collection(
            collection_name=TEST_COLLECTION
        )

    qdrant_client.create_collection(
        collection_name=TEST_COLLECTION,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE,
        ),
    )


def generate_documents():
    documents = []

    for document_id in range(1, DOCUMENT_COUNT + 1):
        for chunk_index in range(CHUNKS_PER_DOCUMENT):
            documents.append(
                f"""
                Synapse benchmark document {document_id}.
                This is representative enterprise knowledge content
                used to benchmark document embedding and vector indexing.
                Document category: engineering.
                Chunk number: {chunk_index}.
                The system processes documents through parsing,
                chunking, embedding, and vector indexing.
                """
            )

    return documents


def main():
    print("=" * 60)
    print("SYNAPSE SCALABILITY BENCHMARK")
    print("=" * 60)

    print(f"Documents: {DOCUMENT_COUNT}")
    print(f"Chunks/document: {CHUNKS_PER_DOCUMENT}")
    print(
        f"Total chunks: "
        f"{DOCUMENT_COUNT * CHUNKS_PER_DOCUMENT}"
    )

    create_test_collection()

    texts = generate_documents()

    print("\nLoading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    print("Embedding documents...")

    embedding_start = time.perf_counter()

    vectors = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True,
        batch_size=32,
    )

    embedding_time = (
        time.perf_counter() - embedding_start
    )

    print(
        f"\nEmbedding time: "
        f"{embedding_time:.2f} seconds"
    )

    print("\nIndexing vectors into temporary Qdrant collection...")

    points = []

    for index, vector in enumerate(vectors):
        document_id = (
            index // CHUNKS_PER_DOCUMENT
        ) + 1

        chunk_index = (
            index % CHUNKS_PER_DOCUMENT
        )

        points.append(
            PointStruct(
                id=index + 1,
                vector=vector.tolist(),
                payload={
                    "document_id": document_id,
                    "chunk_id": index + 1,
                    "chunk_index": chunk_index,
                    "user_id": 4,
                    "filename": (
                        f"benchmark_{document_id}.txt"
                    ),
                    "source_type": "TEXT",
                },
            )
        )

    indexing_start = time.perf_counter()

    BATCH_SIZE = 256

    for start in range(0, len(points), BATCH_SIZE):
        batch = points[start:start + BATCH_SIZE]

        qdrant_client.upsert(
            collection_name=TEST_COLLECTION,
            points=batch,
        )

    indexing_time = (
        time.perf_counter() - indexing_start
    )

    total_time = (
        embedding_time + indexing_time
    )

    print(
        f"Qdrant indexing time: "
        f"{indexing_time:.2f} seconds"
    )

    print(
        f"Total embedding + indexing time: "
        f"{total_time:.2f} seconds"
    )

    print("\n===== THROUGHPUT =====")

    print(
        f"Documents/sec: "
        f"{DOCUMENT_COUNT / total_time:.2f}"
    )

    print(
        f"Chunks/sec: "
        f"{len(texts) / total_time:.2f}"
    )

    print("\nVerifying indexed points...")

    collection_info = qdrant_client.get_collection(
        TEST_COLLECTION
    )

    print(
        f"Indexed vectors: "
        f"{collection_info.points_count}"
    )

    print("\nCleaning up temporary collection...")

    qdrant_client.delete_collection(
        collection_name=TEST_COLLECTION
    )

    del vectors
    del points
    gc.collect()

    print("Benchmark complete.")


if __name__ == "__main__":
    main()