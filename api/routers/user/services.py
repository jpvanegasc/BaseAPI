from typing import List

from fastapi import APIRouter, Depends

from api.common import db_session, object_response, MessageException
from api.common.utils import message_response
import api.controllers.user as user_controllers
import api.schemas.user as user_schemas

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post("")
def create_user(new_user: user_schemas.UserCreate, db=Depends(db_session)):
    existing = user_controllers.get_user_by_username(db, new_user.username)

    if existing:
        raise MessageException("user already exists")

    new_user = user_controllers.create_user(db, new_user.dict())
    return object_response(user_schemas.User.from_orm(new_user).dict(), status_code=201)


@router.get("")
def get_all_users(db=Depends(db_session)):
    all_users = user_controllers.get_all_users(db)
    return object_response(
        [user_schemas.User.from_orm(user).dict() for user in all_users]
    )


@router.get("/{user_id}")
def get_user_by_id(user_id, db=Depends(db_session)):
    user = user_controllers.get_user_by_id(db, user_id)
    return object_response(user_schemas.User.from_orm(user).dict())


@router.patch("/{user_id}")
def edit_user(user_id, update_data: user_schemas.UserUpdate, db=Depends(db_session)):
    updated_user = user_controllers.edit_user(db, user_id, update_data.dict())
    return object_response(
        user_schemas.User.from_orm(updated_user).dict(exclude_none=True)
    )


@router.delete("/{user_id}")
def delete_user(user_id, db=Depends(db_session)):
    user_controllers.delete_user(db, user_id)
    return message_response("Deleted user")
