from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio


async def test_sign_in_login_error(make_post_request):
    # Попытка входа с ошибкой в логине.
    response = await make_post_request(f'action/sign_in')


async def test_sign_in_password_error(make_post_request):
    # Попытка входа с ошибкой в пароле.
    response = await make_post_request(f'action/sign_in')


async def test_sign_in(make_post_request):
    # Вход зарегистрированного пользователя.
    response = await make_post_request(f'action/sign_in')
