import json
from dataclasses import dataclass
from typing import Optional

import aiohttp
import aioredis
import pytest
from elasticsearch import AsyncElasticsearch, RequestError
from elasticsearch.helpers import async_bulk
from multidict import CIMultiDictProxy

from .settings import CONFIG
from .testdata.fake_models import FakeFilm, FakeGenre, FakePerson

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
    with open(f'functional/testdata/{file_name}.json', 'r') as index:
        data = json.load(index)
        # TODO  The 'body' parameter is deprecated and will be removed in a future version.
        # Instead use individual parameters.
        await es_client.indices.create(index=index_name, body=data)


@pytest.fixture()
async def generate_docs(es_client):
    # Фикстура для генерации фейковых данных, которые используются для тестов.
    madman_mode = False
    test_indices = {'movies': 'movies', 'genres': 'genres', 'persons': 'persons'}

    # Создание индексов для тестов.
    for index, file_name in test_indices.items():
        try:
            await create_index(es_client, file_name=file_name, index_name=index)
        except RequestError:
            # Тесты на рабочих индексах? Ок...
            madman_mode = True

    # Генерация персон, жанров и фильмов.
    fake_persons = [FakePerson() for _ in range(20)]
    fake_genres = [
        FakeGenre(name)
        for name in ['Фэнтези', 'Комедия', 'Триллер', 'Приключения', 'Боевик', 'Аниме', 'Мюзикл']
    ]
    fake_films = [FakeFilm(fake_persons, fake_genres) for _ in range(10)]

    films = get_index_data(index='movies', fake_docs=fake_films)
    genres = get_index_data(index='genres', fake_docs=fake_genres)
    persons = get_index_data(index='persons', fake_docs=fake_persons)

    # Запись фейковых данных в эластик.
    await async_bulk(es_client, films+genres+persons)
    yield {'films': films, 'genres': genres, 'persons': persons}

    if madman_mode:
        # Аккуратно удаляем фейковые данные, стараясь не задеть рабочие...
        docs_to_delete = [{'_op_type': 'delete', '_index': 'movies', '_id': doc['_id']} for doc in films]
        docs_to_delete.extend([{'_op_type': 'delete', '_index': 'genres', '_id': doc['_id']} for doc in genres])
        docs_to_delete.extend([{'_op_type': 'delete', '_index': 'persons', '_id': doc['_id']} for doc in persons])
        await async_bulk(es_client, docs_to_delete)
    else:
        # Удаление тестовых индексов. Ведь тестовых, да?
        for index in test_indices.keys():
            await es_client.indices.delete(index=index)


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
