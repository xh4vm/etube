import asyncio
from dataclasses import dataclass
from typing import Any, Optional
from urllib.parse import urlencode

import aiohttp
import pytest
import psycopg2

from multidict import CIMultiDictProxy
from psycopg2.extras import DictCursor, register_uuid

from .settings import CONFIG
from .utils.data_generators.postgres.user import UserDataGenerator
from .utils.data_generators.postgres.role import RoleDataGenerator
from .utils.data_generators.postgres.permission import PermissionDataGenerator
from .utils.data_generators.postgres.user_role import UserRoleDataGenerator
from .utils.data_generators.postgres.role_permission import RolePermissionDataGenerator


SERVICE_URL = f'{CONFIG.API.URL}:{CONFIG.API.PORT}'


@dataclass
class HTTPResponse:
    body: dict[str, Any]
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope='session')
async def pg_cursor():
    conn = psycopg2.connect(**CONFIG.DB.dsn(), cursor_factory=DictCursor)

    _pg_cursor = conn.cursor() 
        
    with open(f'{CONFIG.BASE_DIR}/{CONFIG.DB.SCHEMA_FILE_NAME}', 'r') as schema_fd:
        _pg_cursor.execute(schema_fd.read())

    register_uuid()
    
    yield _pg_cursor

    _pg_cursor.close()
    conn.close()


@pytest.fixture(scope='session')
async def session():
    connector = aiohttp.TCPConnector(force_close=True)
    session = aiohttp.ClientSession(connector=connector)
    yield session
    await session.close()


@pytest.fixture
def make_post_request(session):
    async def inner(method: str, json: Optional[dict] = None, headers: Optional[dict] = None) -> HTTPResponse:
        json = json or {}
        headers = headers or {}
        
        url = SERVICE_URL + f'{CONFIG.API.API_PATH}/{CONFIG.API.API_VERSION}/' + method
        async with session.post(url, json=json, headers=headers) as response:
            return HTTPResponse(body=await response.json(), headers=response.headers, status=response.status,)

    return inner


@pytest.fixture
def make_request(session):
    async def inner(
            method: str,
            target: str,
            params: Optional[dict] = None,
            headers: Optional[dict] = None,
            data: Optional[dict] = None,
    ) -> HTTPResponse:
        params = params or {}
        headers = headers or {}
        data = data or {}
        url = SERVICE_URL + f'{CONFIG.API.API_PATH}/{CONFIG.API.API_VERSION}/' + target + '?' + urlencode(params)
        async with getattr(session, method)(url, json=data, headers=headers) as response:
            return HTTPResponse(body=await response.json(), headers=response.headers, status=response.status,)

    return inner


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def generate_users(pg_cursor):

    user_dg = UserDataGenerator(conn=pg_cursor)

    yield await user_dg.load()

    await user_dg.clean()


@pytest.fixture(scope='session')
async def generate_roles(pg_cursor):
    role_dg = RoleDataGenerator(conn=pg_cursor)
    yield await role_dg.load()
    await role_dg.clean()


@pytest.fixture(scope='session')
async def generate_permissions(pg_cursor):
    permission_dg = PermissionDataGenerator(conn=pg_cursor)
    yield await permission_dg.load()
    await permission_dg.clean()


@pytest.fixture(scope='session')
async def generate_user_roles(pg_cursor):
    user_role_dg = UserRoleDataGenerator(conn=pg_cursor)
    yield await user_role_dg.load()
    await user_role_dg.clean()


@pytest.fixture(scope='session')
async def generate_role_permissions(pg_cursor):
    role_permission_dg = RolePermissionDataGenerator(conn=pg_cursor)
    yield await role_permission_dg.load()
    await role_permission_dg.clean()
