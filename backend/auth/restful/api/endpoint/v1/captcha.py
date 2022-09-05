from http import HTTPStatus
from random import randrange

from api.app import spec
from api.errors.captcha import CaptchaError
from api.schema.base import CaptchaTask
from api.schema.captcha.check import (CaptchaCheckBodyParams,
                                      CaptchaCheckHeader, CaptchaCheckResponse)
from api.schema.captcha.create import CaptchaCreateHeader
from api.utils.decorators import json_response, unpack_models
from api.utils.system import json_abort
from core.config import CAPTCHA_CONFIG
from flask import Blueprint, Response, make_response

bp = Blueprint('captcha', __name__, url_prefix='/captcha')
TAG = 'Captcha'


@bp.route('', methods=['GET'])
@spec.validate(
    headers=CaptchaCreateHeader, tags=[TAG],
)
@unpack_models
def create_captcha(headers: CaptchaCreateHeader,) -> Response:
    """ Страница капчи
    ---
    """

    task = CaptchaTask(parameter=randrange(-1000, 1000), message='Вычислите тангенс числа')
    return make_response(
        {'parameter': task.parameter, 'message': task.message},
        200,
        {
            'data_signature': task.sig(secret=CAPTCHA_CONFIG.SECRET),
            'redirect_url': headers.redirect_url,
            'redirect_data': headers.redirect_data,
        },
    )


@bp.route('', methods=['POST'])
@spec.validate(
    body=CaptchaCheckBodyParams, headers=CaptchaCheckHeader, tags=[TAG],
)
@unpack_models
@json_response
def check_captcha(body: CaptchaCheckBodyParams, headers: CaptchaCheckHeader,) -> CaptchaCheckResponse:
    """ Страница ответа на задачу капчи
    ---
    """

    signature = headers.data_signature
    if signature is None:
        json_abort(HTTPStatus.BAD_REQUEST, CaptchaError.SIGNATURE_DOES_NOT_EXIST)

    task = CaptchaTask(parameter=body.parameter, message=body.message, answer=body.answer)

    if not task.sig_check(signature=signature, secret=CAPTCHA_CONFIG.SECRET):
        json_abort(HTTPStatus.UNPROCESSABLE_ENTITY, CaptchaError.NOT_VALID_SIGNATURE)

    return CaptchaCheckResponse(
        message='Вы решили слишком сложную для человека задачу. Вы робот, но мы Вам доверяем.',
        redirect_url=headers.redirect_url,
        redirect_data=headers.redirect_data,
    )
