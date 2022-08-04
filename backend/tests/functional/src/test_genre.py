import orjson
import pytest
from ..settings import CacheSettings


@pytest.mark.asyncio
async def test_genre_details(redis_client, generate_docs, make_get_request):
    # Проверка поиска жанра по id (ответ 200 и полнота основных данных).
    await redis_client.flushall()
    genre_for_test = generate_docs.genres[0]
    genre_id = genre_for_test['_id']
    main_fields = ['id', 'name', 'description']
    response = await make_get_request(f'genre/{genre_id}')

    assert response.status == 200

    for field in main_fields:
        assert response.body[field] == genre_for_test['_source'][field]


@pytest.mark.asyncio
async def test_genre_films_list(redis_client, generate_docs, make_get_request):
    # Выборочная проверка поля "Фильмы" при поиске жанра.
    await redis_client.flushall()
    # Берем жанр из первого фильма, чтобы избежать ситуации,
    # когда выбрали жанр без единого фильма.
    genre_for_test = generate_docs.films[0]['_source']['genres'][0]
    films_with_genre = generate_docs.films_with_genre
    genre_id = genre_for_test['id']
    response = await make_get_request(f'genre/{genre_id}')
    genre_films = response.body['films']
    for film in films_with_genre:
        genre_films.remove(film)

    assert genre_films == []


@pytest.mark.asyncio
async def test_genre_error(redis_client, make_get_request):
    # Поиск несуществующего жанра.
    await redis_client.flushall()
    genre_id = '0123456789'
    response = await make_get_request(f'genre/{genre_id}')

    assert response.status == 404


@pytest.mark.asyncio
async def test_genre_sort(redis_client, make_get_request):
    # Проверка правильности сортировки.
    await redis_client.flushall()
    response = await make_get_request(f'genres?sort=name.raw')
    genres_in_response = [genre['name'] for genre in response.body['items']]

    assert genres_in_response == sorted(genres_in_response)


@pytest.mark.asyncio
async def test_genre_cache(redis_client, generate_docs, make_get_request):
    # Проверка работы системы кэширования.
    await redis_client.flushall()
    genre_for_test = generate_docs.genres[0]
    genre_id = genre_for_test['_id']
    elastic_response = await make_get_request(f'genre/{genre_id}')
    cache_key = CacheSettings.get_doc_id_cache('genres', genre_id)
    redis_response = await redis_client.get(cache_key)
    elastic_data = elastic_response.body
    redis_data = orjson.loads(redis_response)['_source']
    main_fields = ['id', 'name', 'description']
    for field in main_fields:
        assert redis_data[field] == elastic_data[field]
