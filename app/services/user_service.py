from sqlalchemy.orm import Session

from app.auth.hashing import hash_password
from app.models.user import User
from app.schemas.user import UserCreate


def create_user(
    db: Session,
    user: UserCreate,
) -> User:

    db_user = User(
        full_name=user.full_name,
        email=user.email,
        hashed_password=hash_password(user.password),
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user