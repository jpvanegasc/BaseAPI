from sqlalchemy import Column, String

from api.common.database import Base, PkModel, CRUDMixin
from api.common.utils import get_password_hash


class User(Base, PkModel, CRUDMixin):
    __tablename__ = "users"

    username = Column(String(), unique=True)
    password = Column(String())

    def __init__(self, *args, **kwargs) -> None:
        if kwargs.get("password"):
            kwargs["password"] = get_password_hash(kwargs["password"])
        super().__init__(*args, **kwargs)
