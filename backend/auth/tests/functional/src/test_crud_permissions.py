import pytest

from ..utils.auth.jwt import create_token
from functional.settings import CONFIG

pytestmark = pytest.mark.asyncio
claims={'sub': '6f2819c9-957b-45b6-8348-853f71bb6adf', 'login': 'cheburashka'}

# В тесте создания разрешения создается новый объект, который затем надо удалить.
created_permission_id = ''

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

    assert len(response.body.get('permissions')) == 2


async def test_create_permission(make_request):
    # Создание разрешения.
    response = await make_request(
        method='post',
        target=f'auth/manager/permission',
        json={
            'title': 'get user',
            "description": 'permission description',
            "http_method": 'GET',
            'url': 'permission url',
        },
        headers={CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}'},
    )
    global created_permission_id
    created_permission_id = response.body.get('id')

    assert response.body.get('message') == 'Разрешение get user создано.'


async def test_create_existing_permission(make_request):
    # Создание существующего разрешения.
    response = await make_request(
        method='post',
        target=f'auth/manager/permission',
        json={
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
    json = {
       'id': 'b8ac6615-012f-4469-ad03-cc87a42db5e0',
       'title': 'create user',
       "description": '',
       "http_method": 'POST',
       'url': '',
   }
    response = await make_request(
        method='put',
        target=f'auth/manager/permission',
        json=json,
        headers={CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}'},
    )

    assert response.body.get('__root__') == json


async def test_remove_permission(make_request, generate_permissions):
    # Удаление разрешения.
    response = await make_request(
        method='delete',
        target=f'auth/manager/permission',
        json={
            'id': created_permission_id,
        },
        headers={CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}'},
    )

    assert response.body.get('message') == f'Разрешение {created_permission_id} удалено.'
