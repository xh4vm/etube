from functools import wraps
from flask import abort, jsonify, request

from auth_client.src.utils import header_token_extractor
from auth_client.exceptions.access import AccessException


def json_response(f):
    """Декоратор который после выполнения функции из Response-модели делает json и возвращает ее."""

    @wraps(f)
    def decorated_function(*args, **kwargs):
        result_dict = f(*args, **kwargs)
        return jsonify(**result_dict.dict(by_alias=True))

    return decorated_function


def unpack_models(f):
    """Декоратор который входные модели укладывает в kwargs функции."""

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if (body := request.context.body) is not None:
            kwargs.update({'body': body})

        if (query := request.context.query) is not None:
            kwargs.update({'query': query})

        if (headers := request.context.headers) is not None:
            kwargs.update({'headers': headers})

        return f(*args, **kwargs)

    return decorated_function


def token_extractor(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        kwargs['token'] = header_token_extractor(request)

        return f(*args, **kwargs)

    return decorated_function


def access_exception_handler(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except AccessException as access_exception:
            abort(access_exception.status, access_exception.message)
    return decorated_function
