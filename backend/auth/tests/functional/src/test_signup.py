from http import HTTPStatus

import pytest

pytestmark = pytest.mark.asyncio


async def test_sign_up_not_full_data(make_request):
    # Попытка регистрации с неполными данными.
    response = await make_request(
        method='post',
        target=f'auth/action/sign_up',
        json={'login': 'new_user'}
    )
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_sign_up(make_request):
    # Регистрация нового пользователя.
    response = await make_request(
        method='post',
        target=f'auth/action/sign_up',
        json={
            'login': 'new_user',
            'email': 'mail@mail.ru',
            'password': '123qwe',
        }
    )

    assert response.status == HTTPStatus.OK
    assert response.body['message'] == 'Пользователь успешно зарегистрирован.'


async def test_sign_up_login_error(make_request):
    # Попытка регистрации с уже зарегистрированной почтой.
    response = await make_request(
        method='post',
        target=f'auth/action/sign_up',
        json={
            'login': 'new_user',
            'email': 'mail@mail.ru',
            'password': '123qwe',
        }
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body['message'] == 'Пользователь с такой почтой уже существует.'
