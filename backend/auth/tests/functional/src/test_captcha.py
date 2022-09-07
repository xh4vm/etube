from http import HTTPStatus

import pytest
from functional.settings import CAPTCHA_CONFIG

from ..utils.errors.captcha import CaptchaError
from ..utils.fake_models.captcha import FakeCaptchaTask

pytestmark = pytest.mark.asyncio


async def test_captcha(make_request):
    # Проверка капчи. Правильный ответ
    task = FakeCaptchaTask(parameter=10, message='Вычислите тангенс угла')

    response = await make_request(
        method='post',
        target='auth/captcha',
        json=task.dict(),
        headers={
            'Data-Signature': task.sig(secret=CAPTCHA_CONFIG.SECRET),
            'Redirect-Url': 'some url',
            'Redirect-Data': 'some data',
        },
    )

    assert response.status == HTTPStatus.OK
    assert response.body.get('redirect_url') is not None


async def test_captcha_error(make_request):
    # Проверка капчи. Неправильный ответ
    task = FakeCaptchaTask(parameter=10, message='Вычислите тангенс угла')

    response = await make_request(
        method='post',
        target='auth/captcha',
        json={'parameter': task.parameter, 'message': task.message, 'answer': 1.12},
        headers={
            'Data-Signature': task.sig(secret=CAPTCHA_CONFIG.SECRET),
            'Redirect-Url': 'some url',
            'Redirect-Data': 'some data',
        },
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body.get('message') == CaptchaError.NOT_VALID_SIGNATURE
