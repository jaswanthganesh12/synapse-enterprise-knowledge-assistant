from datetime import datetime
from fastapi import UploadFile
from fastapi import BackgroundTasks

from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    title: str
    source_type: str
    status: str

    model_config = {
        "from_attributes": True
    }


class UploadResponse(BaseModel):
    message: str
    document: DocumentResponse