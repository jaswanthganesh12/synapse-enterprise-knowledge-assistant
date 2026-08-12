from dataclasses import dataclass, field
from typing import Any


@dataclass
class DocumentChunk:
    text: str
    chunk_index: int
    metadata: dict[str, Any] = field(default_factory=dict)