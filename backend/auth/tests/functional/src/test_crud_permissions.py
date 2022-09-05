import hashlib
from datetime import datetime
from http import HTTPStatus

import pytest
from functional.settings import CONFIG

from ..utils.auth.jwt import create_token
from ..utils.fake_models.base import fake
from ..utils.fake_models.permission import FakePermission

pytestmark = pytest.mark.asyncio
url = f'{CONFIG.API.HOST}:{CONFIG.API.PORT}/api/v1/auth/manager/permission'
claims = {
    'sub': '6f2819c9-957b-45b6-8348-853f71bb6adf',
    'login': 'cheburashka',
    'exp': int(datetime.timestamp(datetime.now()) + 100),
    'permissions': {hashlib.md5(url.encode(), usedforsecurity=False).hexdigest(): ['GET', 'POST', 'PUT', 'DELETE'], },
}


async def test_get_user_permissions(
    make_request, generate_users, generate_roles, generate_permissions, generate_user_roles, generate_role_permissions,
):
    # Получение разрешений пользователя.
    response = await make_request(
        method='get',
        target='auth/manager/permission',
        headers={CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}', 'User-Agent': fake.chrome()},
    )

    assert response.status == HTTPStatus.OK

    recv_perms = response.body.get('permissions')
    assert len(recv_perms) == 3
    assert {perm.get('title') for perm in recv_perms} == {'create user', 'update user', 'remove user'}


async def test_create_permission(make_request, pg_cursor):
    # Создание разрешения.
    perm = FakePermission()
    response = await make_request(
        method='post',
        target='auth/manager/permission',
        json={
            'title': perm.title,
            'description': perm.description,
            'http_method': perm.http_method,
            'url': perm.url,
        },
        headers={CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}', 'User-Agent': fake.chrome()},
    )

    delete_statement = f"DELETE FROM {CONFIG.DB.SCHEMA_NAME}.permissions WHERE title = '{perm.title}';"
    pg_cursor.execute(delete_statement)

    assert response.status == HTTPStatus.OK
    assert response.body.get('message') == f'Разрешение {perm.title} создано.'


async def test_create_existing_permission(
    make_request, generate_permissions,
):
    # Создание существующего разрешения.
    perm = FakePermission(title='create user')
    response = await make_request(
        method='post',
        target='auth/manager/permission',
        json={
            'title': perm.title,
            'description': perm.description,
            'http_method': perm.http_method,
            'url': perm.url,
        },
        headers={CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}', 'User-Agent': fake.chrome()},
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body.get('message') == 'Разрешение уже существует.'


async def test_update_permission(make_request, generate_permissions):
    # Обновление разрешения.
    perm = FakePermission()
    json = {
        'id': 'b8ac6615-012f-4469-ad03-cc87a42db5e0',
        'title': perm.title,
        'description': perm.description,
        'http_method': perm.http_method,
        'url': perm.url,
    }
    response = await make_request(
        method='put',
        target='auth/manager/permission',
        json=json,
        headers={CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}', 'User-Agent': fake.chrome()},
    )

    assert response.status == HTTPStatus.OK
    assert response.body.get('__root__') == json


async def test_remove_permission(make_request, generate_permissions):
    # Удаление разрешения.
    response = await make_request(
        method='delete',
        target='auth/manager/permission',
        json={'id': 'b8ac6615-012f-4469-ad03-cc87a42db5e0', },
        headers={CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}', 'User-Agent': fake.chrome()},
    )

    assert response.status == HTTPStatus.OK
    assert response.body.get('message') == 'Разрешение b8ac6615-012f-4469-ad03-cc87a42db5e0 удалено.'
