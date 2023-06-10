from uuid import UUID
from typing import Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import db_session
from app.models import User
from app.services import user as user_service
from app.exceptions import UserNotFound, DuplicateUser


def valid_user(external_id: UUID, db: Session = Depends(db_session)) -> Optional[User]:
    if user := user_service.get_by_external_id(db, external_id):
        return user

    raise UserNotFound()


