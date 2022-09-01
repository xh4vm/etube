import hashlib
import hmac
from http import HTTPStatus
from math import tan
from random import randrange

import pytest
from functional.settings import OAUTH_CONFIG

pytestmark = pytest.mark.asyncio


async def test_captcha(make_request):
    # Проверка капчи. Правильный ответ
    x = randrange(-1000, 1000)
    answer = round(tan(x), 3)
    data_string = f"x='{x}' answer='{answer}'"
    signature = hmac.new(bytes(OAUTH_CONFIG.SECRET, 'utf-8'), msg=bytes(data_string, 'utf-8'),
                    digestmod=hashlib.sha256).hexdigest()
    response = await make_request(
        method='post',
        target=f'auth/captcha',
        json={'x': x, 'answer': answer},
        headers={'data_signature': signature, 'redirect_url': 'some url', 'redirect_data': 'some data'},
    )

    assert response.status == HTTPStatus.OK
    assert response.body.get('redirect_url') is not None


async def test_captcha_error(make_request):
    # Проверка капчи. Неправильный ответ
    x = randrange(-1000, 1000)
    answer = round(tan(x), 3)
    data_string = f"x='{x}' answer='{answer+1}'"
    signature = hmac.new(bytes(OAUTH_CONFIG.SECRET, 'utf-8'), msg=bytes(data_string, 'utf-8'),
                    digestmod=hashlib.sha256).hexdigest()
    response = await make_request(
        method='post',
        target=f'auth/captcha',
        json={'x': x, 'answer': answer},
        headers={'data_signature': signature, 'redirect_url': 'some url', 'redirect_data': 'some data'},
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
