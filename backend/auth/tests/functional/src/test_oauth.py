import hashlib
import hmac
import json

import pytest

from http import HTTPStatus

from functional.settings import CONFIG

pytestmark = pytest.mark.asyncio


async def test_sign_in_yandex(make_request, pg_cursor):
    # Авторизация через Яндекс.
    user_service_id = '12345'
    user_email = 'test@mail.com'
    client_secret = CONFIG.YANDEX.CLIENT_SECRET
    message = '{}{}'.format(user_service_id, user_email)
    secret = hmac.new(bytes(client_secret, 'utf-8'), msg=bytes(message, 'utf-8'),
                         digestmod=hashlib.sha256).hexdigest()
    user_data = json.dumps({'user_service_id': user_service_id, 'email': user_email, 'secret': secret})
    response = await make_request(
        method='get', target=f'auth/action/sign_in/yandex?user_data={user_data}',
    )
    delete_statement = (
        f"DELETE FROM {CONFIG.DB.SCHEMA_NAME}.users WHERE email = '{user_email}';"
    )
    pg_cursor.execute(delete_statement)

    assert response.status == HTTPStatus.OK
    assert response.body.get('access_token') is not None


async def test_sign_in_yandex_error(make_request):
    # Попытка авторизации с неверным хэш-кодом
    secret = '59a4ccae59ed72416109e17d659c949049f584e2c4d24229f54a60883fb6e277'
    user_data = json.dumps({'user_service_id': '12345', 'email': 'test@mail.com', 'secret': secret})
    response = await make_request(
        method='get', target=f'auth/action/sign_in/yandex?user_data={user_data}',
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body.get('access_token') is None


async def test_sign_in_vk(make_request, pg_cursor):
    # Авторизация через VK.
    user_service_id = '12345'
    user_email = 'test@mail.com'
    client_secret = CONFIG.VK.CLIENT_SECRET
    message = '{}{}'.format(user_service_id, user_email)
    secret = hmac.new(bytes(client_secret, 'utf-8'), msg=bytes(message, 'utf-8'),
                         digestmod=hashlib.sha256).hexdigest()
    user_data = json.dumps({'user_service_id': user_service_id, 'email': user_email, 'secret': secret})
    response = await make_request(
        method='get', target=f'auth/action/sign_in/vk?user_data={user_data}',
    )
    delete_statement = (
        f"DELETE FROM {CONFIG.DB.SCHEMA_NAME}.users WHERE email = '{user_email}';"
    )
    pg_cursor.execute(delete_statement)

    assert response.status == HTTPStatus.OK
    assert response.body.get('access_token') is not None


async def test_sign_in_vk_error(make_request):
    # Попытка авторизации с неверным хэш-кодом
    secret = '59a4ccae59ed72416109e17d659c949049f584e2c4d24229f54a60883fb6e277'
    user_data = json.dumps({'user_service_id': '12345', 'email': 'test@mail.com', 'secret': secret})
    response = await make_request(
        method='get', target=f'auth/action/sign_in/vk?user_data={user_data}',
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body.get('access_token') is None
