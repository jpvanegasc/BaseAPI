from typing import Any
from pydantic import BaseModel
from passlib.context import CryptContext
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

BASE_RESPONSE = {"data": None, "message": ""}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def object_response(
    item: Any,
    status_code: int = 200,
    message: str = "Success",
    schema: BaseModel = None,
    exclude_none: bool = False,
):
    response = BASE_RESPONSE.copy()

    if schema:
        if isinstance(item, list):
            item = [schema.from_orm(i).dict(exclude_none=exclude_none) for i in item]
        else:
            item = schema.from_orm(item).dict(exclude_none=exclude_none)

    response["data"] = item
    response["message"] = message

    response = jsonable_encoder(response)

    return JSONResponse(response, status_code=status_code)


def message_response(message: str, status_code: int = 200):
    response = BASE_RESPONSE.copy()

    response["message"] = message

    return JSONResponse(response, status_code=status_code)


class MessageException(Exception):
    def __init__(self, message, status_code=400, reason=None) -> None:
        self.message = message
        self.status_code = status_code
        self.reason = reason

    def to_dict(self):
        response = BASE_RESPONSE.copy()

        response["message"] = self.message
        if self.reason:
            response["reason"] = self.reason

        return response


def get_password_hash(plain_password):
    return pwd_context.hash(plain_password)


def check_password_hash(plain_password, password_hash):
    return pwd_context.verify(plain_password, password_hash)
