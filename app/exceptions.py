from fastapi import HTTPException, status


class DetailException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = None
    headers = None

    def __init__(self) -> None:
        super().__init__(self.status_code, self.detail, self.headers)


class UserNotFound(DetailException):
    status_code = 404
    detail = "user not found"


class DuplicateUser(DetailException):
    detail = "duplicate user"
