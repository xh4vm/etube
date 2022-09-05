from http import HTTPStatus

import pytest
from functional.settings import CAPTCHA_CONFIG
from ..utils.fake_models.captcha import FakeCaptchaTask
from ..utils.errors.captcha import CaptchaError

pytestmark = pytest.mark.asyncio


async def test_captcha(make_request):
    # Проверка капчи. Правильный ответ
    task = FakeCaptchaTask(parameter=10, message='Вычислите тангенс угла')
    
    response = await make_request(
        method='post',
        target=f'auth/captcha',
        json=task.dict(),
        headers={
            'data_signature': task.sig(secret=CAPTCHA_CONFIG.SECRET), 
            'redirect_url': 'some url', 
            'redirect_data': 'some data'
        },
    )

    assert response.status == HTTPStatus.OK
    assert response.body.get('redirect_url') is not None


async def test_captcha_error(make_request):
    # Проверка капчи. Неправильный ответ
    task = FakeCaptchaTask(parameter=10, message='Вычислите тангенс угла')
    
    response = await make_request(
        method='post',
        target=f'auth/captcha',
        json={'parameter': task.parameter, 'message': task.message, 'answer': 1.12},
        headers={
            'data_signature': task.sig(secret=CAPTCHA_CONFIG.SECRET), 
            'redirect_url': 'some url', 
            'redirect_data': 'some data'
        },
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body.get('message') == CaptchaError.NOT_VALID_SIGNATURE
