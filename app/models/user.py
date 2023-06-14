from uuid import uuid4

from sqlalchemy import Column, String, DateTime, Integer, Uuid
from sqlalchemy.sql import func

from app.database import Base
from app.utils import get_password_hash


class User(Base):
    """User

    Attributes:
        id : int
            Primary key, used internally.
        external_id : uuid.UUID
            External identifier for the user. This is the value exposed to the public.
        username : str
            Username of the user.
        password : str
            User's password. Hashed at creation time.
        created_at : datetime.datetime)
            The timestamp when the user was created.
        updated_at : datetime.datetime)
            The timestamp when the user was last updated.
    """

    __tablename__ = "user"

    id = Column(Integer(), primary_key=True, index=True)
    external_id = Column(Uuid, unique=True, default=lambda: str(uuid4()))

    username = Column(String, unique=True, index=True)
    password = Column(String)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, *args, **kwargs) -> None:
        if kwargs.get("password"):
            kwargs["password"] = get_password_hash(kwargs["password"])
        super().__init__(*args, **kwargs)
