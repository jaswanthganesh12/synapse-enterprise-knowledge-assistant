from enum import Enum


class DocumentStatus(str, Enum):
    UPLOADED = "UPLOADED"
    PROCESSING = "PROCESSING"
    INDEXED = "INDEXED"
    FAILED = "FAILED"


class SourceType(str, Enum):
    PDF = "PDF"
    SLACK = "SLACK"
    CONFLUENCE = "CONFLUENCE"
    NOTION = "NOTION"