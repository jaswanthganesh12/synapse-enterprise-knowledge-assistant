from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
)
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.dependencies import get_db
from app.models.user import User
from app.schemas.document import UploadResponse
from app.services.document_service import upload_document


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)
