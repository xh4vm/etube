from elasticsearch.helpers import async_bulk
from ..utils.fake_docs import generate_docs, del_docs

import pytest


@pytest.mark.asyncio
async def test_film_details(redis_client, es_client, make_get_request):
    # Проверка поиска фильма по id.
    await async_bulk(es_client, generate_docs(index='movies'))
    response = await make_get_request('film/123')
    assert response.status == 200
    await async_bulk(es_client, del_docs(index='movies'))


@pytest.mark.asyncio
async def test_film_error(redis_client, es_client, make_get_request):
    # Поиск несуществующего фильма.
    # ?search='Не существующий фильм'
    # response = {"next_page":null,"prev_page":null,"page":1,"page_size":50,"total":0,"items":[]}
    pass


@pytest.mark.asyncio
async def test_films_filter(redis_client, es_client, make_get_request):
    # Проверка фильтров.
    # ?filter=genre 1
    # Убедиться, что в выдачу попали фейковые фильмы с указанными жанрами.
    pass


@pytest.mark.asyncio
async def test_films_sort(redis_client, es_client, make_get_request):
    # Проверка правильности сортировки.
    # ?sort=imdb_rating:desc
    # Проверить рейтинги первых 50 фильмов (должны располагаться по нисходящей).
    pass


@pytest.mark.asyncio
async def test_films_cache(redis_client, es_client, make_get_request):
    # Проверка работы системы кэширования.
    # await make_get_request('film/123')
    # await redis_client('film/123')
    pass
