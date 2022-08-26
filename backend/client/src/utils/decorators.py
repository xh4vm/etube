from functools import wraps
from fastapi import HTTPException, Request
from auth_client.src.utils import header_token_extractor
from auth_client.exceptions.access import AccessException


def token_extractor(f):
    @wraps(f)
    def decorated_function(*args, request: Request, **kwargs):
        kwargs['token'] = header_token_extractor(request=request)

        return f(*args, **kwargs)

    return decorated_function


def access_exception_handler(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except AccessException as access_exception:
            raise HTTPException(status_code=access_exception.status, detail=access_exception.message)
    return decorated_function
