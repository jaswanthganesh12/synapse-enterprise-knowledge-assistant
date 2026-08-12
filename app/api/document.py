from pathlib import Path

from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.db.dependencies import get_db
from app.models.user import User
from app.schemas.document import UploadResponse
from app.services.document_service import (
    attach_file_to_document,
    create_document_record,
)
from app.storage.file_service import save_uploaded_file


router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


ALLOWED_MIME_TYPES = {
    "application/pdf": "PDF",
    "text/plain": "TEXT",
    "text/markdown": "MARKDOWN",
}


@router.post(
    "/upload",
    response_model=UploadResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def upload_document(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type",
        )

    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required",
        )

    title = Path(file.filename).stem
    source_type = ALLOWED_MIME_TYPES[file.content_type]

    document = create_document_record(
        db=db,
        title=title,
        original_filename=file.filename,
        stored_filename="",
        file_path="",
        mime_type=file.content_type,
        source_type=source_type,
        uploaded_by=current_user.id,
    )

    original_filename, stored_filename, file_path = (
        save_uploaded_file(
            file=file,
            user_id=current_user.id,
            document_id=document.id,
        )
    )

    document = attach_file_to_document(
        db=db,
        document=document,
        original_filename=original_filename,
        stored_filename=stored_filename,
        file_path=file_path,
    )

    return {
        "message": "Document uploaded successfully",
        "document": document,
    }