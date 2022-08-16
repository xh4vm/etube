from functools import wraps
from flask_jwt_extended import verify_jwt_in_request
from http import HTTPStatus

from ..model.models import User
from ..schema.action.sign_in import SignInBodyParams
from ..errors.action.sign_in import SignInActionError
from ..utils.system import json_abort


def already_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        is_verified = False
        try:
            verify_jwt_in_request()
            is_verified = True
        except Exception:
            pass

        if is_verified:
            json_abort(HTTPStatus.OK, SignInActionError.ALREADY_AUTH)

        return f(*args, **kwargs)
    return decorated_function
