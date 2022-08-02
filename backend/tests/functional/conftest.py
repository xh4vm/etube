import asyncio
from dataclasses import dataclass
from asyncio import sleep
from typing import Any, Optional

import aiohttp
import aioredis
import pytest
from elasticsearch import AsyncElasticsearch
from multidict import CIMultiDictProxy

from .settings import CONFIG
from .utils.data_generators.elastic.genre import GenreDataGenerator
from .utils.data_generators.elastic.person import PersonDataGenerator
from .utils.data_generators.elastic.movies import FilmDataGenerator

SERVICE_URL = f'{CONFIG.API.url}:{CONFIG.API.port}'


@dataclass
class HTTPResponse:
    body: dict[str, Any]
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
    client = AsyncElasticsearch([
        (
            f'{CONFIG.ELASTIC.protocol}://{CONFIG.ELASTIC.user}:{CONFIG.ELASTIC.password}'
            f'@{CONFIG.ELASTIC.host}:{CONFIG.ELASTIC.port}'
        )
    ])
    yield client
    await client.close()


@pytest.fixture(scope='session')
async def session():
    session = aiohttp.ClientSession()
    yield session
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
async def generate_genre(es_client):
    genre_dg = GenreDataGenerator(conn=es_client)
    
    yield await genre_dg.load()

    await genre_dg.clean()


@pytest.fixture(scope='session')
async def generate_person(es_client):
    person_dg = PersonDataGenerator(conn=es_client)

    yield await person_dg.load()

    await person_dg.clean()


@pytest.fixture(scope='session')
async def generate_movies(es_client):
    film_dg = FilmDataGenerator(conn=es_client)

    yield await film_dg.load()

    await film_dg.clean()
