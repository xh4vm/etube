import orjson
import pytest
from ..settings import CacheSettings
from ..utils.fake_models.genre import FakeGenreBrief


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
async def test_genre_error(generate_genres, make_get_request):
    # Поиск несуществующего жанра.
    genre_id = '0123456789'
    response = await make_get_request(f'genre/{genre_id}')

    assert response.status == 404


@pytest.mark.asyncio
async def test_genre_sort_name_desc(generate_genres, make_get_request):
    # Проверка правильности сортировки.
    expected_full_map = sorted(generate_genres, key=lambda elem: elem['_source']['name'], reverse=True)
    expected = [FakeGenreBrief.parse_obj(genre['_source']) for genre in expected_full_map]
    
    response = await make_get_request(f'genres', params={'sort': 'name.raw:desc'})

    assert expected == response.body['items']


@pytest.mark.asyncio
async def test_genre_sort_name_asc(generate_genres, make_get_request):
    # Проверка правильности сортировки.
    expected_full_map = sorted(generate_genres, key=lambda elem: elem['_source']['name'])
    expected = [FakeGenreBrief.parse_obj(genre['_source']) for genre in expected_full_map]
    
    response = await make_get_request(f'genres', params={'sort': 'name.raw'})

    assert expected == response.body['items']


@pytest.mark.asyncio
async def test_genre_cache(redis_client, generate_genres, make_get_request):
    # Проверка работы системы кэширования.
    genre = generate_genres[1]

    elastic_response = await make_get_request(f'genre/{genre["_id"]}')
    elastic_data = elastic_response.body

    cache_key = CacheSettings.get_doc_id_cache('genres', genre["_id"])
    redis_response = await redis_client.get(cache_key)
    redis_data = orjson.loads(redis_response)
    
    assert elastic_data['id'] == redis_data['_source']['id']
    assert elastic_data['name'] == redis_data['_source']['name']
    assert elastic_data['description'] == redis_data['_source']['description']
