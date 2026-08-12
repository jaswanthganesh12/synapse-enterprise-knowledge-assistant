from sentence_transformers import CrossEncoder


MODEL_NAME = "cross-encoder/ms-marco-MiniLM-L-6-v2"

reranker = CrossEncoder(MODEL_NAME)


def rerank(
    query: str,
    documents: list[str],
    top_k: int = 5,
) -> list[tuple[int, float]]:

    pairs = [
        (query, document)
        for document in documents
    ]

    scores = reranker.predict(pairs)

    ranked = sorted(
        enumerate(scores),
        key=lambda item: item[1],
        reverse=True,
    )

    return ranked[:top_k]