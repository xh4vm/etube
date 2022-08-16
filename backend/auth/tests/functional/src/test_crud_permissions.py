import pytest

from ..utils.auth.jwt import create_token
from functional.settings import CONFIG

from flask_jwt_extended import create_access_token

pytestmark = pytest.mark.asyncio
claims={'sub': '6f2819c9-957b-45b6-8348-853f71bb6adf', 'login': 'cheburashka'}

async def test_get_user_permissions(
        make_request,
        generate_users,
        generate_roles,
        generate_permissions,
        generate_user_roles,
        generate_role_permissions,
):
    # Получение разрешений пользователя.
    response = await make_request(
        method='get',
        target='auth/manager/permission',
        params={'user_id': '6f2819c9-957b-45b6-8348-853f71bb6adf'},
        headers={CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}'},
    )

    print('***', response)

    assert len(response.body.get('permissions')) == 2


async def test_create_permission(make_request):
    # Создание разрешения.
    response = await make_request(
        method='post',
        target=f'auth/manager/permission',
        data={
            'title': 'get user',
            "description": 'permission description',
            "http_method": 'GET',
            'url': 'permission url',
        },
        headers={CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}'},
    )

    assert response.body.get('message') == 'Разрешение get user создано.'


async def test_create_existing_permission(make_request):
    # Создание существующего разрешения.
    response = await make_request(
        method='post',
        target=f'auth/manager/permission',
        data={
            'title': 'get user',
            "description": 'permission description',
            "http_method": 'GET',
            'url': 'permission url',
        },
        headers={CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}'},
    )

    assert response.body.get('message') == 'Разрешение get user уже существует.'


async def test_update_permission(make_request, generate_permissions):
    # Обновление разрешения.
    data = {
       'id': 'b8ac6615-012f-4469-ad03-cc87a42db5e0',
       'title': 'create user',
       "description": '',
       "http_method": 'POST',
       'url': '',
   }
    response = await make_request(
        method='put',
        target=f'auth/manager/permission',
        data=data,
        headers={CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}'},
    )

    assert response.body.get('__root__') == data


async def test_remove_permission(make_request, generate_permissions):
    # Удаление разрешения.
    response = await make_request(
        method='delete',
        target=f'auth/manager/permission',
        data={
            'id': '24637592-11a9-403a-8fc0-43363b5c55aa',
        },
        headers={CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}'},
    )

    assert response.body.get('message') == 'Разрешение 24637592-11a9-403a-8fc0-43363b5c55aa удалено.'
