from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio


async def test_sign_up_not_full_data(make_post_request):
    # Попытка регистрации с неполными данными.
    response = await make_post_request(f'action/sign_up')


async def test_sign_up(make_post_request):
    # Регистрация нового пользователя.
    response = await make_post_request(f'action/sign_up')


async def test_sign_up_login_error(make_post_request):
    # Попытка регистрации с уже зарегистрированным логином.
    response = await make_post_request(f'action/sign_up')


async def test_sign_up_email_error(make_post_request):
    # Попытка регистрации с уже зарегистрированным email.
    response = await make_post_request(f'action/sign_up')
