from fastapi import APIRouter, Depends

from api.common import db_session, object_response, MessageException
from api.common.utils import message_response
import api.controllers as controllers
import api.schemas.user as user_schemas

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post("")
def create_user(new_user: user_schemas.UserCreate, db=Depends(db_session)):
    existing = controllers.user.get_by_username(db, new_user.username)

    if existing:
        raise MessageException("user already exists")

    new_user = controllers.user.create(db, new_user.dict())
    return object_response(new_user, status_code=201, schema=user_schemas.UserRead)


@router.get("")
def get_all_users(db=Depends(db_session)):
    all_users = controllers.user.all(db)
    return object_response(all_users, schema=user_schemas.UserRead)


@router.get("/{user_id}")
def get_by_id(user_id, db=Depends(db_session)):
    user = controllers.user.get_by_id(db, user_id)

    if not user:
        raise MessageException("user not found", status_code=404)

    return object_response(user, schema=user_schemas.UserRead)


@router.patch("/{user_id}")
def edit_user(user_id, update_data: user_schemas.UserUpdate, db=Depends(db_session)):
    if not controllers.user.get_by_id(db, user_id):
        raise MessageException("user not found", status_code=404)

    updated_user = controllers.user.update(db, user_id, update_data.dict())
    return object_response(
        updated_user, schema=user_schemas.UserRead, exclude_none=True
    )


@router.delete("/{user_id}")
def delete_user(user_id, db=Depends(db_session)):
    if not controllers.user.get_by_id(db, user_id):
        raise MessageException("user not found", status_code=404)

    controllers.user.delete(db, user_id)
    return message_response("Deleted user")
