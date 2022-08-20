from functools import wraps

from flask import jsonify, request


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
