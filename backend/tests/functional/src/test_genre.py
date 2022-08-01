import orjson
import pytest


@pytest.mark.asyncio
async def test_genre_details(redis_client, generate_genre, make_get_request):
    # Проверка поиска жанра по id (ответ 200 и полнота основных данных).
    await redis_client.flushall()
    expected = generate_genre[0]
    genre_id = expected['_id']
    response = await make_get_request(f'genre/{genre_id}')

    assert response.status == 200

    assert response.body['id'] == expected['_source']['id']
    assert response.body['name'] == expected['_source']['name']
    assert response.body['description'] == expected['_source']['description']


# @pytest.mark.asyncio
# async def test_genre_films_list(redis_client, generate_genre, make_get_request):
#     # Выборочная проверка поля "Фильмы" при поиске жанра.
#     await redis_client.flushall()
#     genre_for_test = generate_genre.data[0]
#     genre_id = genre_for_test['_id']
#     genre_name = genre_for_test['_source']['name']
#     response = await make_get_request(f'genre/{genre_id}')
#     genre_films = response.body['films']
#     film_for_test = genre_films[0]['id']
#     response = await make_get_request(f'film/{film_for_test}')
#     film_genres = response.body['genres_list']

#     assert genre_name in film_genres


# @pytest.mark.asyncio
# async def test_genre_error(redis_client, make_get_request):
#     # Поиск несуществующего жанра.
#     await redis_client.flushall()
#     genre_id = '0123456789'
#     response = await make_get_request(f'genre/{genre_id}')

#     assert response.status == 404


# @pytest.mark.asyncio
# async def test_genre_sort(redis_client, make_get_request):
#     # Проверка правильности сортировки.
#     await redis_client.flushall()
#     response = await make_get_request(f'genres?sort=name.raw')
#     genres_in_response = [genre['name'] for genre in response.body['items']]

#     assert genres_in_response == sorted(genres_in_response)


# @pytest.mark.asyncio
# async def test_genre_cache(redis_client, generate_genre, make_get_request):
#     # Проверка работы системы кэширования.
#     await redis_client.flushall()
#     genre_for_test = generate_genre.data[0]
#     genre_id = genre_for_test['_id']
#     elastic_response = await make_get_request(f'genre/{genre_id}')
#     cache_key = f'genres::detail::{genre_id}'
#     redis_response = await redis_client.get(cache_key)
#     elastic_data = elastic_response.body
#     redis_data = orjson.loads(redis_response)['_source']
#     main_fields = ['id', 'name', 'description']
#     for field in main_fields:
#         assert redis_data[field] == elastic_data[field]
