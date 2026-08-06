from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.models.user import User
from app.auth.permissions import require_role
from fastapi.security import OAuth2PasswordRequestForm

from app.db.dependencies import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import create_user
from fastapi import HTTPException, status

from app.auth.service import login_user
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    return create_user(db, user)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    token = login_user(
        db,
        form_data.username,   # email
        form_data.password,
    )

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return token

@router.get("/me")
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user

@router.get("/admin")
def admin_only(
    current_user: User = Depends(
        require_role("admin")
    ),
):
    return {
        "message": "Welcome Admin",
        "user": current_user.email,
    }