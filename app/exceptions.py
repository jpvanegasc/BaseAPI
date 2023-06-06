from app.utils import BASE_RESPONSE


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
