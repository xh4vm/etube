from flask import abort, make_response, jsonify
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request
from http import HTTPStatus

from ..model.models import User
from ..schema.action.sign_in import SignInBodyParams
from ..errors.action.sign_in import SignInActionError
from ..utils.system import json_abort


def user_required(f):
    @wraps(f)
    def decorated_function(body: SignInBodyParams, *args, **kwargs):

        user = (User
            .query
            .filter_by(login=body.login)
            .first())
        
        if user is None or \
            not user.check_password(body.password):
            json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, SignInActionError.NOT_VALID_AUTH_DATA)

        kwargs['body'] = body
        kwargs['user'] = user

        return f(*args, **kwargs)
    return decorated_function


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
