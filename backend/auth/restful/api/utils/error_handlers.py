from http import HTTPStatus

from flask import jsonify
from werkzeug.exceptions import HTTPException


def many_requests(error: HTTPException):
    return jsonify(error=f'Rate Limit Error: "{error.description}"'), HTTPStatus.TOO_MANY_REQUESTS
