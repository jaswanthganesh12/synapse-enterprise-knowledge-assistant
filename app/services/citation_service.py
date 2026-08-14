def build_citations(
    results: list[dict],
) -> list[dict]:

    citations = []

    seen = set()

    for result in results:
        citation_key = (
            result["document_id"],
            result["chunk_id"],
        )

        if citation_key in seen:
            continue

        seen.add(citation_key)

        citations.append(
            {
                "document_id": result["document_id"],
                "filename": result.get(
                    "filename",
                    "Unknown",
                ),
                "page_number": result.get(
                    "page_number"
                ),
                "chunk_id": result["chunk_id"],
                "source_type": result.get(
                    "source_type",
                    "Unknown",
                ),
            }
        )

    return citations