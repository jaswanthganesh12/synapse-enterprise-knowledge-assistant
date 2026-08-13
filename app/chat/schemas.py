from pydantic import BaseModel


class ChatRequest(BaseModel):
    query: str
    conversation_id: int


class Citation(BaseModel):
    document_id: int
    filename: str
    page_number: int | None
    chunk_id: int


class ChatResponse(BaseModel):
    answer: str
    citations: list[Citation]