from fastapi.responses import JSONResponse

BASE_RESPONSE = {"data": None, "message": ""}


def object_response(item, status_code=200, message="Success"):
    response = BASE_RESPONSE.copy()

    response["data"] = item
    response["message"] = message

    return JSONResponse(response, status_code=status_code)


def message_response(message, status_code=200):
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
