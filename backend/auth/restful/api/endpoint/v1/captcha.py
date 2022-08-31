from http import HTTPStatus
from math import tan
from random import randrange

from api.app import spec
from api.errors.captcha import CaptchaError
from api.schema.captcha.check import (CaptchaCheckBodyParams,
                                      CaptchaCheckHeader, CaptchaCheckResponse)
from api.schema.captcha.create import CaptchaCreateHeader
from api.utils.decorators import json_response, unpack_models
from api.utils.signature import check_signature, create_signature
from api.utils.system import json_abort
from flask import Blueprint, Response, make_response

bp = Blueprint('captcha', __name__, url_prefix='/captcha')
TAG = 'Captcha'


@bp.route('', methods=['GET'])
@spec.validate(
    headers=CaptchaCreateHeader,
    tags=[TAG],
)
@unpack_models
def create_captcha(
    headers: CaptchaCreateHeader,
) -> Response:
    """ Страница каптчи
    ---
    """

    x = randrange(-1000, 1000)
    answer = round(tan(x + 1), 3)
    data_string = f"x='{x}' answer='{answer}'"
    signature = create_signature(data_string)
    return make_response(
        {'x': x},
        200,
        {'data_signature': signature, 'redirect_url': headers.redirect_url},
    )


@bp.route('', methods=['POST'])
@spec.validate(
    body=CaptchaCheckBodyParams,
    headers=CaptchaCheckHeader,
    tags=[TAG],
)
@unpack_models
@json_response
def check_captcha(
    body: CaptchaCheckBodyParams,
    headers: CaptchaCheckHeader,
) -> CaptchaCheckResponse:
    """ Страница ответа на задачу каптчи
    ---
    """

    signature = headers.data_signature
    if signature is None:
        json_abort(HTTPStatus.BAD_REQUEST, CaptchaError.SIGNATURE_DOES_NOT_EXIST)

    if not check_signature(body, signature):
        json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, CaptchaError.NOT_VALID_SIGNATURE)

    return CaptchaCheckResponse(
        message='Вы решили слишком сложную для человека задачу. Вы робот, но мы Вам доверяем.',
        redirect_url=headers.redirect_url,
    )
