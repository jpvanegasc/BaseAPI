from uuid import UUID
from typing import List

from pydantic import BaseModel

from app.schemas.common import optional, PagedResponse


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    external_id: UUID

    class Config:
        orm_mode = True


class UserPagedResponse(PagedResponse):
    items: List[UserRead]


@optional
class UserUpdate(UserBase):
    pass
