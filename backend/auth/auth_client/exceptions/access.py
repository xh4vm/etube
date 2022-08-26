from http.client import HTTPException


class AccessException(HTTPException):
    def __init__(self, status: int, message: str):
        self.status = status
        self.message = message
