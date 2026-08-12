from app.chunking.models import DocumentChunk
from app.parsers.base import ParsedDocument


def chunk_document(
    document: ParsedDocument,
    chunk_size: int = 500,
    overlap: int = 100,
) -> list[DocumentChunk]:

    if overlap >= chunk_size:
        raise ValueError(
            "Overlap must be smaller than chunk size"
        )

    chunks = []
    chunk_index = 0

    for page in document.pages:
        text = page.text.strip()

        if not text:
            continue

        start = 0

        while start < len(text):
            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(
                    DocumentChunk(
                        text=chunk_text,
                        chunk_index=chunk_index,
                        metadata={
                            **document.metadata,
                            "page_number": page.page_number,
                        },
                    )
                )

                chunk_index += 1

            start += chunk_size - overlap

    return chunks