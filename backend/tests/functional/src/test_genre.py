import orjson
import pytest
import hashlib


@pytest.mark.asyncio
async def test_genre_details(redis_client, generate_movies, generate_genre, make_get_request):
    # Проверка поиска жанра по id (ответ 200 и полнота основных данных).
    await redis_client.flushall()
    expected = generate_genre[0]
    response = await make_get_request(f'genre/{expected["_id"]}')

    assert response.status == 200

    assert response.body['id'] == expected['_source']['id']
    assert response.body['name'] == expected['_source']['name']
    assert response.body['description'] == expected['_source']['description']
    assert response.body['films'] == expected['_source']['films']


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
async def test_genre_cache(redis_client, generate_genre, make_get_request):
    # Проверка работы системы кэширования.
    await redis_client.flushall()
    genre = generate_genre[0]

    elastic_response = await make_get_request(f'genre/{genre["_id"]}')
    elastic_data = elastic_response.body

    cache_key = f'genres::detail::{genre["_id"]}'
    redis_response = await redis_client.get(cache_key)
    redis_data = orjson.loads(redis_response)
    
    assert elastic_data['id'] == redis_data['_source']['id']
    assert elastic_data['name'] == redis_data['_source']['name']
    assert elastic_data['description'] == redis_data['_source']['description']
