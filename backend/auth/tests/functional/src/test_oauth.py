from http import HTTPStatus

import pytest
from functional.settings import CONFIG, OAUTH_CONFIG

from ..utils.fake_models.user import FakeUserSocial

pytestmark = pytest.mark.asyncio


async def test_sign_in_yandex(make_request, pg_cursor):
    # Авторизация через Яндекс.
    user_social = FakeUserSocial(service_name='yandex')

    response = await make_request(
        method='post',
        target='auth/action/sign_in/oauth',
        json=user_social.dict(),
        headers={'X-Integrity-Token': user_social.sig(secret=OAUTH_CONFIG.SECRET)},
    )

    delete_statement = f"DELETE FROM {CONFIG.DB.SCHEMA_NAME}.users WHERE email = '{user_social.email}';"
    pg_cursor.execute(delete_statement)

    assert response.status == HTTPStatus.OK
    assert response.body.get('access_token') is not None


async def test_sign_in_yandex_error(make_request):
    # Попытка авторизации с неверным хэшем
    user_social = FakeUserSocial(service_name='yandex')
    bad_sig = '59a4ccae59ed72416109e17d659c949049f584e2c4d24229f54a60883fb6e277'

    response = await make_request(
        method='post',
        target='auth/action/sign_in/oauth',
        json=user_social.dict(),
        headers={'X-Integrity-Token': bad_sig},
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body.get('message') == 'Неправильная подпись данных'


async def test_sign_in_vk(make_request, pg_cursor):
    # Авторизация через VK.
    user_social = FakeUserSocial(service_name='vk')

    response = await make_request(
        method='post',
        target='auth/action/sign_in/oauth',
        json=user_social.dict(),
        headers={'X-Integrity-Token': user_social.sig(secret=OAUTH_CONFIG.SECRET)},
    )
    delete_statement = f"DELETE FROM {CONFIG.DB.SCHEMA_NAME}.users WHERE email = '{user_social.email}';"
    pg_cursor.execute(delete_statement)

    assert response.status == HTTPStatus.OK
    assert response.body.get('access_token') is not None


async def test_sign_in_vk_error(make_request):
    # Попытка авторизации с неверным хэшем
    user_social = FakeUserSocial(service_name='vk')
    bad_sig = '59a4ccae59ed72416109e17d659c949049f584e2c4d24229f54a60883fb6e277'

    response = await make_request(
        method='post',
        target='auth/action/sign_in/oauth',
        json=user_social.dict(),
        headers={'X-Integrity-Token': bad_sig},
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body.get('message') == 'Неправильная подпись данных'
