import pytest
import uuid
from datetime import datetime
from http import HTTPStatus

from ..utils.auth.jwt import get_jwt_claims, get_jwt_identity, verify_exp_jwt, create_token
from ..utils.errors.token import TokenError

pytestmark = pytest.mark.asyncio


async def test_refresh_token_success(make_request, generate_users, redis_client):
    # Успешный рефреш токена.
    refresh_token = create_token(claims={
        'sub': '6f2819c9-957b-45b6-8348-853f71bb6adf', 
        'type': 'refresh',
    })
    
    response = await make_request(
        method='post',
        target=f'auth/token/refresh', 
        headers={'X-Authorization-Token': f'Bearer {refresh_token}'}
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


async def test_refresh_token_expired_error(make_request, generate_users):
    # Токен протух.
    refresh_token = create_token(
        claims={
            'type': 'refresh',
            'sub': '6f2819c9-957b-45b6-8348-853f71bb6adf', 
            'exp': int(datetime.timestamp(datetime.now()) - 100)}
    )
    response = await make_request(
        method='post',
        target=f'auth/token/refresh', 
        headers={'X-Authorization-Token': f'Bearer {refresh_token}'}
    )

    assert response.status == HTTPStatus.UNAUTHORIZED
    assert response.body['message'] == TokenError.EXPIRED


async def test_refresh_token_invalid_error(make_request, generate_users):
    # Требуется токен.
    access_token = create_token(
        claims={'sub': '6f2819c9-957b-45b6-8348-853f71bb6adf', 'exp': datetime.timestamp(datetime.now())}
    )
    response = await make_request(
        method='post',
        target=f'auth/token/refresh', 
        headers={'X-Authorization-Token': f'Bearer {access_token}'}
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body['message'] == TokenError.INVALID
