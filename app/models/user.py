from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func

from app.database import Base, PkModel, CRUDMixin
from app.utils import get_password_hash


class User(Base, PkModel, CRUDMixin):
    __tablename__ = "user"

    username = Column(String(), unique=True)
    password = Column(String())

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __init__(self, *args, **kwargs) -> None:
        if kwargs.get("password"):
            kwargs["password"] = get_password_hash(kwargs["password"])
        super().__init__(*args, **kwargs)
