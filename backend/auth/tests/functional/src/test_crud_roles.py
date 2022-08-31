from datetime import datetime
from http import HTTPStatus
import hashlib

import pytest
from functional.settings import CONFIG

from ..utils.auth.jwt import create_token
from ..utils.errors.role import RolesError
from ..utils.fake_models.role import FakeRole
from ..utils.fake_models.base import fake

pytestmark = pytest.mark.asyncio
url = f'{CONFIG.API.HOST}:{CONFIG.API.PORT}/api/v1/auth/manager/role'
claims = {
    'sub': '6f2819c9-957b-45b6-8348-853f71bb6adf',
    'login': 'cheburashka',
    'exp': int(datetime.timestamp(datetime.now()) + 100),
    'permissions': {
        hashlib.md5(url.encode(), usedforsecurity=False).hexdigest(): ['GET', 'POST', 'PUT', 'DELETE'],
        hashlib.md5((url + '/permission').encode(), usedforsecurity=False).hexdigest(): ['POST', 'DELETE']
    },
}


async def test_get_roles(
    make_request, generate_users, generate_roles, generate_permissions, generate_user_roles, generate_role_permissions,
):
    # Получение ролей пользователя.
    response = await make_request(
        method='get',
        target='auth/manager/role',
        headers={
            CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}',
            'User-Agent': fake.chrome()
        },
    )

    assert response.status == HTTPStatus.OK

    roles_recv = response.body.get('roles')
    assert len(roles_recv) == 2
    assert {role.get('title') for role in roles_recv} == {'admin', 'moderator'}


async def test_create_role(make_request, pg_cursor):
    # Создание роли.
    role = FakeRole()
    response = await make_request(
        method='post',
        target='auth/manager/role',
        json={'title': role.title, 'description': role.description, },
        headers={
            CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}',
            'User-Agent': fake.chrome()
        },
    )

    delete_statement = f"DELETE FROM {CONFIG.DB.SCHEMA_NAME}.roles WHERE title = '{role.title}';"
    pg_cursor.execute(delete_statement)

    assert response.status == HTTPStatus.OK
    assert response.body.get('message') == f'Роль {role.title} создана.'


async def test_create_existing_role(make_request, generate_roles):
    # Создание существующей роли.
    role = FakeRole(title='admin')
    response = await make_request(
        method='post',
        target='auth/manager/role',
        json={'title': role.title, 'description': role.description, },
        headers={
            CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}',
            'User-Agent': fake.chrome()
        },
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body.get('message') == RolesError.ALREADY_EXISTS


async def test_update_role(make_request, generate_roles):
    # Обновление роли.
    role = FakeRole(id='61cac47c-4e9d-49a1-bf0b-9bfd99953f00', title='super admin')
    response = await make_request(
        method='put',
        target='auth/manager/role',
        json={'id': role.id, 'title': role.title, 'description': role.description, },
        headers={
            CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}',
            'User-Agent': fake.chrome()
        },
    )

    assert response.status == HTTPStatus.OK
    assert response.body.get('__root__')['title'] == role.title


async def test_update_not_found_role(make_request, generate_roles):
    # Обновление роли.
    role = FakeRole(title='super admin')
    response = await make_request(
        method='put',
        target='auth/manager/role',
        json={'id': role.id, 'title': role.title, 'description': role.description, },
        headers={
            CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}',
            'User-Agent': fake.chrome()
        },
    )

    assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.body.get('message') == RolesError.NOT_EXISTS


async def test_set_permissions(make_request, generate_roles, generate_permissions, pg_cursor):
    # Добавление разрешения.
    role_id = 'a6f46c67-a08c-4fb5-9b08-b87b6995c953'
    permission_id = '24637592-11a9-403a-8fc0-43363b5c55aa'

    select_statement = (
        f'SELECT id FROM {CONFIG.DB.SCHEMA_NAME}.role_permissions WHERE '
        f" role_id = '{role_id}' AND permission_id = '{permission_id}';"
    )

    pg_cursor.execute(select_statement)
    assert pg_cursor.fetchone() is None

    response = await make_request(
        method='post',
        target='auth/manager/role/permission',
        json={'role_id': role_id, 'permission_id': permission_id},
        headers={
            CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}',
            'User-Agent': fake.chrome()
        },
    )

    assert response.status == HTTPStatus.OK

    pg_cursor.execute(select_statement)
    assert pg_cursor.fetchone() is not None


async def test_retrieve_permissions(make_request, generate_roles, generate_permissions, pg_cursor):
    # Добавление разрешения.
    role_id = 'a6f46c67-a08c-4fb5-9b08-b87b6995c953'
    permission_id = '58f3e1ae-aba4-414f-9d07-eb4375bd0881'

    select_statement = (
        f'SELECT id FROM {CONFIG.DB.SCHEMA_NAME}.role_permissions WHERE '
        f" role_id = '{role_id}' AND permission_id = '{permission_id}';"
    )

    pg_cursor.execute(select_statement)
    assert pg_cursor.fetchone() is not None

    response = await make_request(
        method='delete',
        target='auth/manager/role/permission',
        json={'role_id': role_id, 'permission_id': permission_id},
        headers={
            CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}',
            'User-Agent': fake.chrome()
        },
    )

    assert response.status == HTTPStatus.OK

    pg_cursor.execute(select_statement)
    assert pg_cursor.fetchone() is None


async def test_remove_role(make_request, generate_roles):
    # Удаление роли.

    response = await make_request(
        method='delete',
        target='auth/manager/role',
        json={'id': '61cac47c-4e9d-49a1-bf0b-9bfd99953f00', },
        headers={
            CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}',
            'User-Agent': fake.chrome()
        },
    )

    assert response.body.get('message') == 'Роль 61cac47c-4e9d-49a1-bf0b-9bfd99953f00 удалена.'
