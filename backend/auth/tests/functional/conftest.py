import asyncio
from dataclasses import dataclass
from typing import Any, Optional

import aiohttp
import pytest
from multidict import CIMultiDictProxy

from .settings import CONFIG

SERVICE_URL = f'{CONFIG.API.url}:{CONFIG.API.port}'


@dataclass
class HTTPResponse:
    body: dict[str, Any]
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_post_request(session):
    async def inner(method: str, params: Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        url = SERVICE_URL + f'{CONFIG.API.api_path}/{CONFIG.API.api_version}/' + method
        async with session.post(url, params=params) as response:
            return HTTPResponse(body=await response.json(), headers=response.headers, status=response.status,)

    return inner


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
