from datetime import datetime
from http import HTTPStatus

import pytest
from functional.settings import CONFIG

from ..utils.auth.jwt import create_token
from ..utils.errors.user import UserError
from ..utils.fake_models.user import FakeUser, fake

pytestmark = pytest.mark.asyncio
claims = {
    'sub': '6f2819c9-957b-45b6-8348-853f71bb6adf',
    'login': 'cheburashka',
    'exp': int(datetime.timestamp(datetime.now()) + 100),
}


async def test_get_user_roles(
    make_request, generate_users, generate_roles, generate_permissions, generate_user_roles, generate_role_permissions,
):
    # Получение пользователей.
    response = await make_request(
        method='get',
        target='auth/manager/user',
        headers={CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}'},
    )

    assert response.status == HTTPStatus.OK

    users_recv = response.body.get('users')
    assert len(users_recv) == 1
    assert {(user.get('login'), user.get('email'),) for user in users_recv} == {('cheburashka', 'chebu@rash.ka',)}


async def test_update_user(make_request, generate_users, pg_cursor):
    # Обновление пользователя.
    password = fake.password()
    user = FakeUser(id='6f2819c9-957b-45b6-8348-853f71bb6adf', login='cheburashka', password=password)
    response = await make_request(
        method='put',
        target='auth/manager/user',
        json={'id': user.id, 'login': user.login, 'email': user.email, 'password': password, },
        headers={CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}'},
    )

    response = await make_request(
        method='put',
        target='auth/manager/user',
        json={'id': user.id, 'login': 'cheburashka', 'email': 'chebu@rash.ka', 'password': '123qwe', },
        headers={CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}'},
    )

    assert response.status == HTTPStatus.OK
    assert response.body.get('__root__').get('login') == user.login


async def test_update_not_found_user(make_request, generate_users):
    # Обновление полльзователя.
    password = fake.password()
    user = FakeUser(title='cheburashka', password=password)
    response = await make_request(
        method='put',
        target='auth/manager/user',
        json={'id': user.id, 'login': user.login, 'email': user.email, 'password': password, },
        headers={CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}'},
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body.get('message') == UserError.NOT_EXISTS


async def test_set_role(make_request, generate_roles, generate_users, pg_cursor):
    role_id = 'a6f46c67-a08c-4fb5-9b08-b87b6995c953'
    user_id = '6f2819c9-957b-45b6-8348-853f71bb6adf'

    select_statement = (
        f"SELECT id FROM {CONFIG.DB.SCHEMA_NAME}.user_roles WHERE role_id = '{role_id}' AND user_id = '{user_id}';"
    )

    pg_cursor.execute(select_statement)
    assert pg_cursor.fetchone() is None

    response = await make_request(
        method='post',
        target='auth/manager/user/role',
        json={'role_id': role_id, 'user_id': user_id},
        headers={CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}'},
    )

    assert response.status == HTTPStatus.OK

    pg_cursor.execute(select_statement)
    assert pg_cursor.fetchone() is not None


async def test_retrieve_role(make_request, generate_users, generate_roles, pg_cursor):
    role_id = 'a6f46c67-a08c-4fb5-9b08-b87b6995c953'
    user_id = '6f2819c9-957b-45b6-8348-853f71bb6adf'

    select_statement = (
        f"SELECT id FROM {CONFIG.DB.SCHEMA_NAME}.user_roles WHERE role_id = '{role_id}' AND user_id = '{user_id}';"
    )

    pg_cursor.execute(select_statement)
    assert pg_cursor.fetchone() is not None

    response = await make_request(
        method='delete',
        target='auth/manager/user/role',
        json={'role_id': role_id, 'user_id': user_id},
        headers={CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}'},
    )

    assert response.status == HTTPStatus.OK

    pg_cursor.execute(select_statement)
    assert pg_cursor.fetchone() is None
