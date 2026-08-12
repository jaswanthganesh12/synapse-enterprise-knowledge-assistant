from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

embedding_model = SentenceTransformer(MODEL_NAME)


def embed_query(text: str) -> list[float]:
    vector = embedding_model.encode(
        text,
        normalize_embeddings=True,
    )

    return vector.tolist()


def embed_texts(
    texts: list[str],
) -> list[list[float]]:
    vectors = embedding_model.encode(
        texts,
        normalize_embeddings=True,
    )

    return vectors.tolist()