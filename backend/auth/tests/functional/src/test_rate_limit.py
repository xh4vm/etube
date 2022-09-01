from datetime import datetime
from http import HTTPStatus
import hashlib

import pytest
from functional.settings import CONFIG

from ..utils.auth.jwt import create_token
from ..utils.errors.user import UserError
from ..utils.fake_models.user import FakeUser, fake

pytestmark = pytest.mark.asyncio
url = f'{CONFIG.API.HOST}:{CONFIG.API.PORT}/api/v1/auth/manager/user'
claims = {
    'sub': '6f2819c9-957b-45b6-8348-853f71bb6adf',
    'login': 'cheburashka',
    'exp': int(datetime.timestamp(datetime.now()) + 100),
    'permissions': {
        hashlib.md5(url.encode(), usedforsecurity=False).hexdigest(): ['GET', 'POST', 'PUT', 'DELETE'],
        hashlib.md5((url + '/history').encode(), usedforsecurity=False).hexdigest(): ['GET']
    },
}


async def test_rate_limit_root_success(make_request):
    for i in range(2):
        response = await make_request(
            method='get',
            target='auth/manager/user',
            headers={
                CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}',
                'User-Agent': fake.chrome()
            },
        )

    assert response.status == HTTPStatus.OK


async def test_rate_limit_root_many_requests(make_request):
    for i in range(10):
        response = await make_request(
            method='get',
            target='auth/manager/user',
            headers={
                CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}',
                'User-Agent': fake.chrome()
            },
        )

    assert response.status == HTTPStatus.TOO_MANY_REQUESTS
    assert response.body.get('error') == 'Rate Limit Error: "3 per 1 second"'


async def test_rate_limit_action_success(make_request, generate_users):
    for i in range(14):
        response = await make_request(
            method='post', 
            target='auth/action/sign_in', 
            json={'login': 'cheburashka', 'password': '123qwe'},
            headers={'User-Agent': fake.chrome()}
        )

    assert response.status == HTTPStatus.OK


async def test_rate_limit_action_many_requests(make_request, generate_users):
    for i in range(16):
        response = await make_request(
            method='post', 
            target='auth/action/sign_in', 
            json={'login': 'cheburashka', 'password': '123qwe'},
            headers={'User-Agent': fake.chrome()}
        )

    assert response.status == HTTPStatus.TOO_MANY_REQUESTS
    assert response.body.get('error') == 'Rate Limit Error: "15 per 1 minute"'


async def test_rate_limit_sign_in_low_bruteforce(make_request, generate_users):
    for i in range(4):
        response = await make_request(
            method='post', 
            target='auth/action/sign_in', 
            json={'login': 'cheburashka', 'password': 'bad password'},
            headers={'User-Agent': fake.chrome()}
        )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY


async def test_rate_limit_sign_in_bruteforce(make_request, generate_users):
    for i in range(6):
        response = await make_request(
            method='post', 
            target='auth/action/sign_in', 
            json={'login': 'cheburashka', 'password': 'bad password'},
            headers={'User-Agent': fake.chrome()}
        )

    assert response.status == HTTPStatus.TOO_MANY_REQUESTS
    assert response.body.get('error') == 'Rate Limit Error: "5 per 1 minute"'


async def test_rate_limit_sign_in_is_not_a_bot(make_request, generate_users):
    for i in range(2):
        response = await make_request(
            method='post', 
            target='auth/action/sign_in', 
            json={'login': 'cheburashka', 'password': '123qwe'},
            headers={'User-Agent': fake.chrome()}
        )

    assert response.status == HTTPStatus.OK


async def test_rate_limit_sign_in_is_a_bot(make_request, generate_users):
    for i in range(10):
        response = await make_request(
            method='post', 
            target='auth/action/sign_in', 
            json={'login': 'cheburashka', 'password': '123qwe'},
            headers={'User-Agent': 'Test'}
        )

    assert response.status == HTTPStatus.TOO_MANY_REQUESTS
    assert response.body.get('error') == 'Rate Limit Error: "5 per 1 minute"'

