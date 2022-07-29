import pytest


@pytest.mark.asyncio
async def test_film_details(generate_docs, redis_client, es_client, make_get_request):
    # Проверка поиска фильма по id.
    fake_film_id = generate_docs['films'][0]['_id']
    response = await make_get_request(f'film/{fake_film_id}')
    assert response.status == 200


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
