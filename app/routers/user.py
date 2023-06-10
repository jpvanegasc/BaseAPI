from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse

from app.database import db_session
import app.services.user as user_service
import app.schemas.user as user_schemas
from app.dependencies.user import valid_user

router = APIRouter(prefix="/api/users", tags=["Users"])


@router.post(
    "",
    response_model=user_schemas.UserRead,
    responses={
        status.HTTP_201_CREATED: {
            "model": user_schemas.UserRead,
            "description": "Success",
        },
        status.HTTP_400_BAD_REQUEST: {"description": "Duplicate user"},
    },
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
)
def create_user(
    new_user: user_schemas.UserCreate,
    db=Depends(db_session),
):
    return user_service.create_user(db, new_user)


@router.get(
    "",
    response_model=user_schemas.UserPagedResponse,
    responses={
        status.HTTP_200_OK: {
            "model": user_schemas.UserPagedResponse,
            "description": "Success",
        },
    },
    status_code=status.HTTP_200_OK,
    summary="Get all users",
)
def get_all_users(page: int = 1, per_page: int = 10, db=Depends(db_session)):
    users = user_service.get_all_users(db, page_number=page, per_page=per_page)
    user_count = user_service.user_count(db)
    return user_schemas.UserPagedResponse(items=users, total=user_count)


@router.get(
    "/{user_id}",
    response_model=user_schemas.UserRead,
    responses={
        status.HTTP_200_OK: {
            "model": user_schemas.UserRead,
            "description": "Success",
        },
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
    status_code=status.HTTP_200_OK,
    summary="Get a user",
)
def get_by_id(user: user_schemas.UserRead = Depends(valid_user)):
    return user_schemas.UserRead.from_orm(user)


@router.delete(
    "/{user_id}",
    responses={
        status.HTTP_202_ACCEPTED: {"description": "Success"},
        status.HTTP_404_NOT_FOUND: {"description": "User not found"},
    },
    status_code=status.HTTP_202_ACCEPTED,
    summary="Delete a user",
)
def delete_user(
    user=Depends(valid_user),
    db=Depends(db_session),
):
    user_service.delete_user(db, user)
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content="user deleted")
