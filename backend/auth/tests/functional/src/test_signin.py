import pytest

from http import HTTPStatus

from functional.settings import CONFIG

from ..utils.auth.jwt import get_jwt_claims, get_jwt_identity, verify_exp_jwt, create_token
from ..utils.errors.action.sign_in import SignInActionError

pytestmark = pytest.mark.asyncio


async def test_sign_in_password_error(make_post_request, generate_users):
    # Попытка входа с ошибкой в пароле.
    response = await make_post_request(f'auth/action/sign_in', json={'login': 'cheburashka', 'password': 'FailPassword'})

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body['message'] == SignInActionError.NOT_VALID_AUTH_DATA


async def test_sign_in_login_error(make_post_request, generate_users):
    # Попытка входа с ошибкой в логине.
    response = await make_post_request(f'auth/action/sign_in', json={'login': 'asd', 'password': '123qwe'})

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body['message'] == SignInActionError.NOT_VALID_AUTH_DATA


async def test_sign_in_login_success(make_post_request, generate_users):
    # Попытка входа.
    response = await make_post_request(f'auth/action/sign_in', json={'login': 'cheburashka', 'password': '123qwe'})

    assert response.status == HTTPStatus.OK
    assert 'access_token' in response.body.keys()
    assert 'refresh_token' in response.body.keys()
    
    access_token = response.body.get('access_token')
    identity = get_jwt_identity(access_token)
    
    assert '0c09752e-27ef-425a-a8e5-662b2ecf441e' == identity

    claims = get_jwt_claims(access_token)
    
    assert 'cheburashka' == claims.get('login')
    assert 'chebu@rash.ka' == claims.get('email')
    assert verify_exp_jwt(access_token) is True

    refresh_token = response.body.get('refresh_token')
    identity = get_jwt_identity(refresh_token)
    
    assert '0c09752e-27ef-425a-a8e5-662b2ecf441e' == identity
    assert verify_exp_jwt(refresh_token) is True


async def test_sign_in_alredy_auth(make_post_request, generate_users):
    access_token = create_token(claims={'sub': '0c09752e-27ef-425a-a8e5-662b2ecf441e', 'login': 'cheburashka', 'password': '123qwe'})
    response = await make_post_request(
        f'auth/action/sign_in', 
        json={'login': 'cheburashka', 'password': '123qwe'}, 
        headers={'X-Authorization-Token': f'Bearer {access_token}'}
    )

    assert response.status == HTTPStatus.OK
    assert response.body['message'] == SignInActionError.ALREADY_AUTH
