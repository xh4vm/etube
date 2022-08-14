from flask import abort, make_response, jsonify
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request

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
            json_abort(422, SignInActionError.NOT_VALID_AUTH_DATA)

        kwargs['user'] = user

        return f(*args, **kwargs)
    return decorated_function


def already_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        
        try:
           verify_jwt_in_request()
           json_abort(200, SignInActionError.ALREADY_AUTH)
        except:
            pass

        return f(*args, **kwargs)
    return decorated_function
