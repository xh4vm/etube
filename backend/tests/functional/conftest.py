import asyncio
from dataclasses import dataclass
from typing import Optional

import aiohttp
import aioredis
import pytest
from elasticsearch import AsyncElasticsearch
from multidict import CIMultiDictProxy

from .settings import CONFIG
from .utils.fake_data_generator import Generator

SERVICE_URL = f'{CONFIG.API.url}:{CONFIG.API.port}'


@dataclass
class HTTPResponse:
    body: dict
    headers: CIMultiDictProxy[str]
    status: int


@pytest.fixture(scope='session')
async def redis_client():
    client = await aioredis.create_redis_pool((CONFIG.REDIS.host, CONFIG.REDIS.port))
    yield client
    client.close()
    await client.wait_closed()


@pytest.fixture(scope='session')
async def es_client():
    client = AsyncElasticsearch(hosts=f'{CONFIG.ELASTIC.protocol}://{CONFIG.ELASTIC.host}:{CONFIG.ELASTIC.port}')
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def session(generate_docs):
    session = aiohttp.ClientSession()
    yield session
    await generate_docs.remove_fake_data()
    await session.close()


@pytest.fixture
def make_get_request(session):
    async def inner(method: str, params: Optional[dict] = None) -> HTTPResponse:
        params = params or {}
        url = SERVICE_URL + f'{CONFIG.API.api_path}/{CONFIG.API.api_version}/' + method
        async with session.get(url, params=params) as response:
            return HTTPResponse(
                body=await response.json(),
                headers=response.headers,
                status=response.status,
            )

    return inner


@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def generate_docs(es_client):
    generator = Generator(es_client)
    await generator.generate_fake_data()
    yield generator
