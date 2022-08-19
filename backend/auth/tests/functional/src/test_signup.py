from http import HTTPStatus

import pytest

from functional.settings import CONFIG
from ..utils.fake_models.base import fake
from ..utils.fake_models.user import FakeUser 

pytestmark = pytest.mark.asyncio


async def test_sign_up_not_full_data(make_request):
    # Попытка регистрации с неполными данными.

    user = FakeUser()

    response = await make_request(
        method='post',
        target=f'auth/action/sign_up',
        json={'login': user.login}
    )
    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_sign_up(make_request, pg_cursor):
    # Регистрация нового пользователя.
    password = fake.password()
    user = FakeUser(password=password)

    response = await make_request(
        method='post',
        target=f'auth/action/sign_up',
        json={
            'login': user.login,
            'email': user.email,
            'password': password,
        }
    )
    
    delete_statement = f"DELETE FROM {CONFIG.DB.SCHEMA_NAME}.users WHERE login = '{user.login}' AND email = '{user.email}' AND password = '{user.password}';"
    pg_cursor.execute(delete_statement)

    assert response.status == HTTPStatus.OK
    assert response.body['message'] == 'Пользователь успешно зарегистрирован.'


async def test_sign_up_login_error(make_request, generate_users):
    # Попытка регистрации с уже зарегистрированной почтой.

    user = FakeUser(login='cheburashka', email='chebu@rash.ka')

    response = await make_request(
        method='post',
        target=f'auth/action/sign_up',
        json={
            'login': user.login,
            'email': user.email,
            'password': fake.password(),
        }
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body['message'] == 'Пользователь с такой почтой уже существует.'
