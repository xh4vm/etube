from flask import abort, make_response, jsonify


def json_abort(status: int, message: str):
    abort(make_response(jsonify(message=message), status))
