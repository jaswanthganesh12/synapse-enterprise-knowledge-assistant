from pathlib import Path

from app.parsers.base import ParsedDocument, ParsedPage


def parse_markdown(file_path: str) -> ParsedDocument:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Markdown file not found: {file_path}"
        )

    text = path.read_text(
        encoding="utf-8"
    )

    return ParsedDocument(
        text=text,
        pages=[
            ParsedPage(
                page_number=1,
                text=text,
            )
        ],
        metadata={
            "source_type": "MARKDOWN",
            "filename": path.name,
        },
    )