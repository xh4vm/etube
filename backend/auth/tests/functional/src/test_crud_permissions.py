import pytest

from ..utils.auth.jwt import create_bearer_token

pytestmark = pytest.mark.asyncio


async def test_get_user_permissions(make_request):
    # Получение разрешений пользователя.
    response = await make_request(
        method='get',
        target=f'auth/manager/permission?user_id=6f2819c9-957b-45b6-8348-853f71bb6adf',
        headers={'X-Authorization-Token': create_bearer_token()},
    )

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
        headers={'X-Authorization-Token': create_bearer_token()},
    )

    assert response.body.get('message') == 'Разрешение get user создано.'


async def test_create_existing_permission(make_request):
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
        headers={'X-Authorization-Token': create_bearer_token()},
    )

    assert response.body.get('message') == 'Разрешение get user уже существует.'


async def test_update_permission(make_request):
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
        headers={'X-Authorization-Token': create_bearer_token()},
    )

    assert response.body.get('__root__') == data


async def test_remove_permission(make_request):
    # Удаление разрешения.
    response = await make_request(
        method='delete',
        target=f'auth/manager/permission',
        data={
            'id': '24637592-11a9-403a-8fc0-43363b5c55aa',
        },
        headers={'X-Authorization-Token': create_bearer_token()},
    )

    assert response.body.get('message') == 'Разрешение 24637592-11a9-403a-8fc0-43363b5c55aa удалено.'
