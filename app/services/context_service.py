def build_context(results: list[dict]) -> str:
    context_parts = []

    for index, result in enumerate(results, start=1):
        context_parts.append(
            f"""SOURCE {index}
Document: {result.get("filename", "Unknown")}
Document ID: {result["document_id"]}
Page: {result["page_number"]}
Chunk ID: {result["chunk_id"]}
Source Type: {result.get("source_type", "Unknown")}

{result["text"]}"""
        )

    return "\n\n---\n\n".join(context_parts)