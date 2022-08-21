from http import HTTPStatus

import pytest
from functional.settings import CONFIG

from ..utils.auth.jwt import (create_token, get_jti, get_jwt_claims,
                              get_jwt_identity, verify_exp_jwt)
from ..utils.errors.action.sign_in import SignInActionError

pytestmark = pytest.mark.asyncio


async def test_sign_in_password_error(make_request, generate_users):
    # Попытка входа с ошибкой в пароле.
    response = await make_request(
        method='post', target='auth/action/sign_in', json={'login': 'cheburashka', 'password': 'FailPassword'}
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body['message'] == SignInActionError.NOT_VALID_AUTH_DATA


async def test_sign_in_login_error(make_request, generate_users):
    # Попытка входа с ошибкой в логине.
    response = await make_request(
        method='post', target='auth/action/sign_in', json={'login': 'asd', 'password': '123qwe'}
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body['message'] == SignInActionError.NOT_VALID_AUTH_DATA


async def test_sign_in_login_success(make_request, generate_users, redis_client):
    # Попытка входа.
    response = await make_request(
        method='post', target='auth/action/sign_in', json={'login': 'cheburashka', 'password': '123qwe'}
    )

    assert response.status == HTTPStatus.OK
    assert 'access_token' in response.body.keys()
    assert 'refresh_token' in response.body.keys()

    access_token = response.body.get('access_token')
    identity = get_jwt_identity(access_token)

    assert '6f2819c9-957b-45b6-8348-853f71bb6adf' == identity

    claims = get_jwt_claims(access_token)

    assert 'cheburashka' == claims.get('login')
    assert 'chebu@rash.ka' == claims.get('email')
    assert verify_exp_jwt(access_token) is True

    refresh_token = response.body.get('refresh_token')
    identity = get_jwt_identity(refresh_token)

    assert '6f2819c9-957b-45b6-8348-853f71bb6adf' == identity
    assert verify_exp_jwt(refresh_token) is True

    refresh_jti = get_jti(refresh_token)
    assert await redis_client.get(f'refresh_token::{refresh_jti}') is not None


async def test_sign_in_alredy_auth(make_request, generate_users):
    access_token = create_token(claims={'sub': '6f2819c9-957b-45b6-8348-853f71bb6adf', 'login': 'cheburashka'})
    response = await make_request(
        method='post',
        target='auth/action/sign_in',
        json={'login': 'cheburashka', 'password': '123qwe'},
        headers={'X-Authorization-Token': f'Bearer {access_token}'},
    )

    assert response.status == HTTPStatus.OK
    assert response.body['message'] == SignInActionError.ALREADY_AUTH


async def test_sign_in_history_record(make_request, generate_users, pg_cursor):

    select_statement = (
        f'SELECT COUNT(*) FROM {CONFIG.DB.SCHEMA_NAME}.sign_in_history WHERE '
        f" user_id = '6f2819c9-957b-45b6-8348-853f71bb6adf';"
    )

    pg_cursor.execute(select_statement)
    count = pg_cursor.fetchone()[0]

    response = await make_request(
        method='post', target='auth/action/sign_in', json={'login': 'cheburashka', 'password': '123qwe'}
    )

    assert response.status == HTTPStatus.OK

    pg_cursor.execute(select_statement)
    assert pg_cursor.fetchone()[0] == count + 1
