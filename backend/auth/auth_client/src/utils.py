from typing import Optional
from flask import abort, jsonify, make_response, request


def json_abort(status: int, message: str):
    abort(make_response(jsonify(message=message), status))


def get_token_from_headers(header_name: str = 'Authorization') -> Optional[str]:
    token = request.headers.get(header_name)

    if token is None or not isinstance(token, str):
        return None

    header, payload = token.split()

    return payload
