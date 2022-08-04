import orjson
import pytest


@pytest.mark.asyncio
async def test_genre_details(generate_movies, generate_genres, make_get_request):
    # Проверка поиска жанра по id (ответ 200 и полнота основных данных).
    expected = generate_genres[0]
    response = await make_get_request(f'genre/{expected["_id"]}')

    assert response.status == 200

    assert response.body['id'] == expected['_source']['id']
    assert response.body['name'] == expected['_source']['name']
    assert response.body['description'] == expected['_source']['description']
    assert response.body['films'] == expected['_source']['films']


@pytest.mark.asyncio
async def test_genre_error(make_get_request):
    # Поиск несуществующего жанра.
    genre_id = '0123456789'
    response = await make_get_request(f'genre/{genre_id}')

    assert response.status == 404


@pytest.mark.asyncio
async def test_genre_sort(make_get_request):
    # Проверка правильности сортировки.
    response = await make_get_request(f'genres', params={'sort': 'name.raw'})
    genres_in_response = [genre['name'] for genre in response.body['items']]

    assert genres_in_response == sorted(genres_in_response)


@pytest.mark.asyncio
async def test_genre_cache(redis_client, generate_genres, make_get_request):
    # Проверка работы системы кэширования.
    genre = generate_genres[1]

    elastic_response = await make_get_request(f'genre/{genre["_id"]}')
    elastic_data = elastic_response.body

    cache_key = f'genres::detail::{genre["_id"]}'
    redis_response = await redis_client.get(cache_key)
    redis_data = orjson.loads(redis_response)
    
    assert elastic_data['id'] == redis_data['_source']['id']
    assert elastic_data['name'] == redis_data['_source']['name']
    assert elastic_data['description'] == redis_data['_source']['description']
