import pytest

from ..utils.auth.jwt import create_token
from functional.settings import CONFIG

pytestmark = pytest.mark.asyncio
claims={'sub': '6f2819c9-957b-45b6-8348-853f71bb6adf', 'login': 'cheburashka'}

# В тесте создания роли создается новый объект, который затем надо удалить.
created_role_id = ''

async def test_get_user_roles(
        make_request,
        generate_users,
        generate_roles,
        generate_permissions,
        generate_user_roles,
        generate_role_permissions,
):
    # Получение ролей пользователя.
    response = await make_request(
        method='get',
        target='auth/manager/role',
        params={'user_id': '6f2819c9-957b-45b6-8348-853f71bb6adf'},
        headers={CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}'},
    )

    assert len(response.body.get('roles')) == 1
    assert response.body.get('roles')[0]['title'] == 'admin'


async def test_create_role(make_request):
    # Создание роли.
    response = await make_request(
        method='post',
        target=f'auth/manager/role',
        json={
            'title': 'super role',
            "description": 'role description',
        },
        headers={CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}'},
    )
    global created_role_id
    created_role_id = response.body.get('id')

    assert response.body.get('message') == 'Роль super role создана.'
    assert response.body.get('id') == created_role_id


async def test_create_existing_role(make_request):
    # Создание существующей роли.
    response = await make_request(
        method='post',
        target=f'auth/manager/role',
        json={
            'title': 'super role',
            "description": 'role description',
        },
        headers={CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}'},
    )

    assert response.body.get('message') == 'Роль уже существует.'


async def test_update_role(make_request, generate_roles):
    # Обновление роли.
    json = {
       'id': '61cac47c-4e9d-49a1-bf0b-9bfd99953f00',
       'title': 'super admin',
       "description": '',
   }
    response = await make_request(
        method='put',
        target=f'auth/manager/role',
        json=json,
        headers={CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}'},
    )

    assert response.body.get('__root__')['title'] == json['title']


async def test_set_permissions(make_request, generate_roles, generate_permissions):
    # Добавление разрешения.
    response = await make_request(
        method='post',
        target=f'auth/manager/role/permission',
        json={
            'role_id': created_role_id,
            'permission_ids': [
                'b8ac6615-012f-4469-ad03-cc87a42db5e0',
                '58f3e1ae-aba4-414f-9d07-eb4375bd0881',
                '24637592-11a9-403a-8fc0-43363b5c55aa',
            ]
        },
        headers={CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}'},
    )

    assert response.body.get('permissions') == ['create user', 'update user', 'remove user']


async def test_retrieve_permissions(make_request, generate_roles, generate_permissions):
    # Добавление разрешения.
    response = await make_request(
        method='delete',
        target=f'auth/manager/role/permission',
        json={
            'role_id': created_role_id,
            'permission_ids': [
                '58f3e1ae-aba4-414f-9d07-eb4375bd0881',
                '24637592-11a9-403a-8fc0-43363b5c55aa',
            ]
        },
        headers={CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}'},
    )

    assert response.body.get('permissions') == ['create user']


async def test_remove_role(make_request, generate_roles):
    # Удаление роли.
    response = await make_request(
        method='delete',
        target=f'auth/manager/role',
        json={
            'id': created_role_id,
        },
        headers={CONFIG.API.JWT_HEADER_NAME: f'Bearer {create_token(claims=claims)}'},
    )

    assert response.body.get('message') == f'Роль {created_role_id} удалена.'
