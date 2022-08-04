import orjson
import pytest
from ..settings import CacheSettings


@pytest.mark.asyncio
async def test_film_details(redis_client, generate_docs, make_get_request):
    # Проверка поиска фильма по id (ответ 200 и полнота данных).
    film_for_test = generate_docs.films[0]
    film_id = film_for_test['_id']
    response = await make_get_request(f'film/{film_id}')
    fields = [
        'id', 'title', 'imdb_rating', 'directors_names', 'actors_names', 'writers_names', 'genres_list', 'description',
    ]

    assert response.status == 200

    for field in fields:
        assert response.body[field] == film_for_test['_source'][field]


@pytest.mark.asyncio
async def test_film_error(redis_client, make_get_request):
    # Поиск несуществующего фильма.
    await redis_client.flushall()
    film_id = '0123456789'
    response = await make_get_request(f'film/{film_id}')

    assert response.status == 404


@pytest.mark.asyncio
async def test_films_filter(redis_client, generate_docs, make_get_request):
    # Проверка фильтра по жанру (полнота списка фильмов).
    await redis_client.flushall()
    docs = generate_docs
    films = docs.films
    genre_for_test = docs.genres[0]['_source']['name']
    films_with_genre = {film['_id'] for film in films if genre_for_test in film['_source']['genres_list']}

    response = await make_get_request(f'films?filters=genres_list:{genre_for_test}')
    films_in_response = {film['id'] for film in response.body['items']}

    assert films_with_genre.symmetric_difference(films_in_response) == set()


@pytest.mark.asyncio
async def test_films_sort(redis_client, make_get_request):
    # Проверка правильности сортировки.
    await redis_client.flushall()
    response = await make_get_request(f'films?sort=imdb_rating:desc')
    films_in_response = [film['imdb_rating'] for film in response.body['items']]

    assert films_in_response == sorted(films_in_response, reverse=True)


@pytest.mark.asyncio
async def test_films_cache(redis_client, generate_docs, make_get_request):
    # Проверка работы системы кэширования.
    await redis_client.flushall()
    film_for_test = generate_docs.films[0]
    film_id = film_for_test['_id']
    elastic_response = await make_get_request(f'film/{film_id}')
    cache_key = CacheSettings.get_doc_id_cache('movies', film_id)
    redis_response = await redis_client.get(cache_key)
    redis_data = orjson.loads(redis_response)['_source']

    for k, v in elastic_response.body.items():
        assert redis_data[k] == v
