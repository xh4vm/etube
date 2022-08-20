from flask import abort, jsonify, make_response


def json_abort(status: int, message: str):
    abort(make_response(jsonify(message=message), status))
