from uuid import UUID
from typing import Literal, List, Optional

from sqlalchemy.orm.session import Session

from app.models import User
from app.database import paginate, commit_if_unique
from app.schemas.user import UserCreate
from app.exceptions import DuplicateUser


def get_by_external_id(db: Session, external_id: UUID) -> Optional[User]:
    """Get a user by its uuid"""
    return db.query(User).filter_by(external_id=external_id).one_or_none()


def get_by_username(db: Session, username: str) -> Optional[User]:
    """Get a user by its username"""
    return db.query(User).filter_by(username=username).one_or_none()


def create_user(db: Session, user_data: UserCreate, commit=True) -> User:
    """Create a new user

    Returns
    -------
    User :
        Newly created user

    Raises
    ------
    DuplicateUser :
        If the user already exists
    """
    new_user = User(**user_data.dict())
    db.add(new_user)
    if commit:
        commit_if_unique(db, DuplicateUser)
    return new_user


def user_count(db: Session) -> int:
    """Get count for all users in the DB"""
    return db.query(User).count()


def get_all_users(db: Session, page_number=1, per_page=10) -> List[User]:
    """Return a paginated query for all users in the DB"""
    return paginate(db.query(User), page_number=page_number, per_page=per_page)


def delete_user(db: Session, user: User, commit=True) -> Literal[True]:
    """Hard delete a user"""
    db.delete(user)
    if commit:
        db.commit()
    return True
