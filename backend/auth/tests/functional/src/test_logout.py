import pytest
import uuid
from datetime import datetime
from http import HTTPStatus
import orjson

from functional.settings import CONFIG

from ..utils.auth.jwt import get_jwt_claims, get_jwt_identity, verify_exp_jwt, create_token, get_jti
from ..utils.errors.token import TokenError


pytestmark = pytest.mark.asyncio


async def test_logout_success(make_request, redis_client, generate_users):
    # Попытка выхода.
    access_token = create_token(
        claims={
            'sub': '6f2819c9-957b-45b6-8348-853f71bb6adf', 
            'login': 'cheburashka',
            'jti': (access_jti := str(uuid.uuid4()))
        }
    )
    refresh_token = create_token(
        claims={
            'sub': '6f2819c9-957b-45b6-8348-853f71bb6adf', 
            'type': 'refresh',
            'jti': (refresh_jti := str(uuid.uuid4()))
        }
    )

    await redis_client.set(f'refresh_token::6f2819c9-957b-45b6-8348-853f71bb6adf', orjson.dumps([refresh_jti]))
    assert orjson.loads(await redis_client.get('refresh_token::6f2819c9-957b-45b6-8348-853f71bb6adf')) == [refresh_jti]

    response = await make_request(
        method='delete',
        target=f'auth/action/logout', 
        headers={'X-Authorization-Token': f'Bearer {access_token}'},
        json={'refresh_token': refresh_token}
    )

    assert response.status == HTTPStatus.OK
    assert await redis_client.get(f'revoked::token::{access_jti}') is not None
    assert await redis_client.get(f'revoked::token::{refresh_jti}') is not None
    assert orjson.loads(await redis_client.get('refresh_token::6f2819c9-957b-45b6-8348-853f71bb6adf')) == []


async def test_logout_error_double_logoute(make_request, redis_client, generate_users):
    # Попытка выхода.
    access_token = create_token(
        claims={
            'sub': '6f2819c9-957b-45b6-8348-853f71bb6adf', 
            'login': 'cheburashka',
            'jti': (access_jti := str(uuid.uuid4()))
        }
    )
    refresh_token = create_token(
        claims={
            'sub': '6f2819c9-957b-45b6-8348-853f71bb6adf', 
            'type': 'refresh',
            'jti': (refresh_jti := str(uuid.uuid4()))
        }
    )

    await redis_client.set(f'revoked::token::{access_jti}', orjson.dumps(''))
    await redis_client.set(f'revoked::token::{refresh_jti}', orjson.dumps(''))

    response = await make_request(
        method='delete',
        target=f'auth/action/logout', 
        headers={'X-Authorization-Token': f'Bearer {access_token}'},
        json={'refresh_token': refresh_token}
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body['message'] == TokenError.REVOKED
