from pydantic import BaseModel

from api.schemas import optional


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: str

    class Config:
        orm_mode = True


@optional
class UserUpdate(UserBase):
    pass
