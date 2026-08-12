from pathlib import Path

from pypdf import PdfReader

from app.parsers.base import ParsedDocument, ParsedPage


def parse_pdf(file_path: str) -> ParsedDocument:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {file_path}"
        )

    reader = PdfReader(path)

    pages = []
    page_texts = []

    for index, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        pages.append(
            ParsedPage(
                page_number=index,
                text=text,
            )
        )

        if text.strip():
            page_texts.append(text)

    full_text = "\n\n".join(page_texts)

    metadata = {
        "source_type": "PDF",
        "page_count": len(reader.pages),
        "filename": path.name,
    }

    return ParsedDocument(
        text=full_text,
        pages=pages,
        metadata=metadata,
    )