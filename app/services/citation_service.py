def build_citations(
    results: list[dict],
) -> list[dict]:

    if not results:
        return []

    result = results[0]

    return [
        {
            "document_id": result["document_id"],
            "filename": result.get(
                "filename",
                "Unknown",
            ),
            "page_number": result["page_number"],
            "chunk_id": result["chunk_id"],
        }
    ]