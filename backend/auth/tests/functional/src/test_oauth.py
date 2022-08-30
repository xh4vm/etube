import hashlib
import hmac

import pytest

from http import HTTPStatus

from functional.settings import CONFIG, OAUTH_CONFIG

pytestmark = pytest.mark.asyncio


async def test_sign_in_yandex(make_request, pg_cursor):
    # Авторизация через Яндекс.
    user_service_id = '12345'
    user_email = 'test@mail.com'
    secret = OAUTH_CONFIG.SECRET
    message = '{}{}'.format(user_service_id, user_email)
    hash = hmac.new(bytes(secret, 'utf-8'), msg=bytes(message, 'utf-8'),
                         digestmod=hashlib.sha256).hexdigest()
    response = await make_request(
        method='post',
        target=f'auth/action/sign_in/yandex',
        json={'user_service_id': user_service_id, 'email': user_email},
        headers={'user_data_hash': hash},
    )
    delete_statement = (
        f"DELETE FROM {CONFIG.DB.SCHEMA_NAME}.users WHERE email = '{user_email}';"
    )
    pg_cursor.execute(delete_statement)

    assert response.status == HTTPStatus.OK
    assert response.body.get('access_token') is not None


async def test_sign_in_yandex_error(make_request):
    # Попытка авторизации с неверным хэш-кодом
    hash = '59a4ccae59ed72416109e17d659c949049f584e2c4d24229f54a60883fb6e277'
    response = await make_request(
        method='get',
        target=f'auth/action/sign_in/yandex',
        json={'user_service_id': '12345', 'email': 'test@mail.com'},
        headers={'user_data_hash': hash},
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body.get('access_token') is None


async def test_sign_in_vk(make_request, pg_cursor):
    # Авторизация через VK.
    user_service_id = '12345'
    user_email = 'test@mail.com'
    secret = OAUTH_CONFIG.SECRET
    message = '{}{}'.format(user_service_id, user_email)
    hash = hmac.new(bytes(secret, 'utf-8'), msg=bytes(message, 'utf-8'),
                         digestmod=hashlib.sha256).hexdigest()
    response = await make_request(
        method='get',
        target=f'auth/action/sign_in/vk',
        json={'user_service_id': user_service_id, 'email': user_email},
        headers={'user_data_hash': hash},
    )
    delete_statement = (
        f"DELETE FROM {CONFIG.DB.SCHEMA_NAME}.users WHERE email = '{user_email}';"
    )
    pg_cursor.execute(delete_statement)

    assert response.status == HTTPStatus.OK
    assert response.body.get('access_token') is not None


async def test_sign_in_vk_error(make_request):
    # Попытка авторизации с неверным хэш-кодом
    hash = '59a4ccae59ed72416109e17d659c949049f584e2c4d24229f54a60883fb6e277'
    response = await make_request(
        method='get',
        target=f'auth/action/sign_in/vk',
        json={'user_service_id': '12345', 'email': 'test@mail.com'},
        headers={'user_data_hash': hash},
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body.get('access_token') is None
