from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.database import db_session
from app.exceptions import UserNotFound, DuplicateUser
import app.services as services
import app.schemas.user as user_schemas

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post(
    "",
    # TODO: add more details
)
def create_user(new_user: user_schemas.UserCreate, db=Depends(db_session)):
    existing = services.user.get_by_username(db, new_user.username)

    if existing:
        raise DuplicateUser()

    return services.user.create(db, new_user.dict())


@router.get("")
def get_all_users(db=Depends(db_session)):
    return services.user.all(db)


@router.get("/{user_id}")
def get_by_id(user_id, db=Depends(db_session)):

    if not (user := services.user.get_by_id(db, user_id)):
        raise UserNotFound()

    return user


@router.patch("/{user_id}")
def edit_user(user_id, update_data: user_schemas.UserUpdate, db=Depends(db_session)):
    if not services.user.get_by_id(db, user_id):
        raise UserNotFound()

    return services.user.update(db, user_id, update_data.dict())


@router.delete("/{user_id}")
def delete_user(user_id, db=Depends(db_session)):
    if not services.user.get_by_id(db, user_id):
        raise UserNotFound()

    services.user.delete(db, user_id)
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content="user deleted")
