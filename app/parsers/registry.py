from app.parsers.pdf_parser import parse_pdf
from app.parsers.text_parser import parse_text
from app.parsers.markdown_parser import parse_markdown


PARSER_REGISTRY = {
    "PDF": parse_pdf,
    "TEXT": parse_text,
    "MARKDOWN": parse_markdown,
}