from passlib.context import CryptContext
from sqlalchemy import Column, String, LargeBinary

from api.common.database import Base, PkModel, CRUDMixin

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base, PkModel, CRUDMixin):
    __tablename__ = "users"

    username = Column(String(), unique=True)
    password = Column(String())

    def __init__(self, *args, **kwargs) -> None:
        if kwargs.get("password"):
            kwargs["password"] = self.get_password(kwargs["password"])
        super().__init__(*args, **kwargs)

    def get_password(self, plain_password):
        return pwd_context.hash(plain_password)

    def check_password(self, plain_password):
        return pwd_context.verify(plain_password, self.password)
