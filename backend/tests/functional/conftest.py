import json

import aioredis
import aiohttp
import pytest

from typing import Optional
from elasticsearch import AsyncElasticsearch

from dataclasses import dataclass
from multidict import CIMultiDictProxy

from .settings import CONFIG
from .testdata.fake_models import FakeFilm, FakeGenre, FakePerson
from elasticsearch.helpers import async_bulk

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
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


def get_index_data(index: str, fake_docs: list) -> list:
    # Структура индексов.
    return [
        {
            '_index': index,
            '_id': doc.id,
            '_source': doc.__dict__
        }
        for doc in fake_docs
    ]


async def create_index(es_client, file_name: str, index_name: str) -> None:
    # Создание индексов.
    with open(f'functional/testdata/{file_name}.json', 'r') as movies_index:
        data = json.load(movies_index)
        await es_client.indices.create(index=index_name, body=data)


@pytest.fixture()
async def generate_docs(es_client):
    # Генерация фейковых данных, которые используются для тестов.
    # TODO Оптимизировать код функции.

    # [
    #     await create_index(es_client, file_name=name, index_name=name)
    #     for name in ['movies', 'genres', 'persons']
    # ]

    fake_persons = [FakePerson() for _ in range(20)]
    fake_genres = [
        FakeGenre(name)
        for name in ['Фэнтези', 'Комедия', 'Триллер', 'Приключения', 'Боевик', 'Аниме', 'Мюзикл']
    ]
    fake_films = [FakeFilm(fake_persons, fake_genres) for _ in range(10)]

    films = get_index_data(index='movies', fake_docs=fake_films)
    genres = get_index_data(index='genres', fake_docs=fake_genres)
    persons = get_index_data(index='persons', fake_docs=fake_persons)

    await async_bulk(es_client, films+genres+persons)
    yield {'films': films, 'genres': genres, 'persons': persons}

    # await es_client.indices.delete(index='movies')
    # await es_client.indices.delete(index='genres')
    # await es_client.indices.delete(index='persons')

    docs_to_delete = [{'_op_type': 'delete', '_index': 'movies', '_id': doc['_id']} for doc in films]
    docs_to_delete.extend([{'_op_type': 'delete', '_index': 'genres', '_id': doc['_id']} for doc in genres])
    docs_to_delete.extend([{'_op_type': 'delete', '_index': 'persons', '_id': doc['_id']} for doc in persons])

    await async_bulk(es_client, docs_to_delete)


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
