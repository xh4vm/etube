import orjson
import pytest

from ..settings import CacheSettings
from ..utils.fake_models.film import FakeFilmBrief


@pytest.mark.asyncio
async def test_film_details(generate_movies, make_get_request):
    # Проверка поиска фильма по id (ответ 200 и полнота данных).
    expected = generate_movies[0]
    response = await make_get_request(f'film/{expected["_id"]}')

    assert response.status == 200
    assert response.body['id'] == expected['_source']['id']
    assert response.body['title'] == expected['_source']['title']
    assert response.body['description'] == expected['_source']['description']
    assert response.body['imdb_rating'] == expected['_source']['imdb_rating']
    assert response.body['directors_names'] == expected['_source']['directors_names']
    assert response.body['actors_names'] == expected['_source']['actors_names']
    assert response.body['writers_names'] == expected['_source']['writers_names']
    assert response.body['genres_list'] == expected['_source']['genres_list']


@pytest.mark.asyncio
async def test_film_error(generate_movies, make_get_request):
    # Поиск несуществующего фильма.
    film_id = '0123456789'
    response = await make_get_request(f'film/{film_id}')

    assert response.status == 404


@pytest.mark.asyncio
async def test_films_filter(generate_movies, generate_genres, make_get_request):
    # Проверка фильтра по жанру (полнота списка фильмов).
    genre_filter = generate_genres[0]['_source']['name']

    films = generate_movies
    expected = [
        FakeFilmBrief.parse_obj(film['_source']) for film in films if genre_filter in film['_source']['genres_list']
    ]

    response = await make_get_request('films', params={'filters': f'genres_list:{genre_filter}'})

    assert response.body['items'] == expected


@pytest.mark.asyncio
async def test_films_sort_imdb_rating_desc(generate_movies, make_get_request):
    # Проверка правильности сортировки.
    expected_full_map = sorted(generate_movies, key=lambda elem: elem['_source']['imdb_rating'], reverse=True)
    expected = [FakeFilmBrief.parse_obj(film['_source']) for film in expected_full_map]

    response = await make_get_request('films', params={'sort': 'imdb_rating:desc'})

    assert expected == response.body['items']


@pytest.mark.asyncio
async def test_films_sort_imdb_rating_asc(generate_movies, make_get_request):
    # Проверка правильности сортировки.
    expected_full_map = sorted(generate_movies, key=lambda elem: elem['_source']['imdb_rating'])
    expected = [FakeFilmBrief.parse_obj(film['_source']) for film in expected_full_map]

    response = await make_get_request('films', params={'sort': 'imdb_rating'})

    assert expected == response.body['items']


@pytest.mark.asyncio
async def test_films_sort_title_desc(generate_movies, make_get_request):
    # Проверка правильности сортировки.
    expected_full_map = sorted(generate_movies, key=lambda elem: elem['_source']['title'], reverse=True)
    expected = [FakeFilmBrief.parse_obj(film['_source']) for film in expected_full_map]

    response = await make_get_request('films', params={'sort': 'title.raw:desc'})

    assert expected == response.body['items']


@pytest.mark.asyncio
async def test_films_sort_title_asc(generate_movies, make_get_request):
    # Проверка правильности сортировки.
    expected_full_map = sorted(generate_movies, key=lambda elem: elem['_source']['title'])
    expected = [FakeFilmBrief.parse_obj(film['_source']) for film in expected_full_map]

    response = await make_get_request('films', params={'sort': 'title'})

    assert expected == response.body['items']


@pytest.mark.asyncio
async def test_films_cache(redis_client, generate_movies, make_get_request):
    # Проверка работы системы кэширования.
    film = generate_movies[0]
    elastic_response = await make_get_request(f'film/{film["_id"]}')

    cache_key = CacheSettings.get_doc_id_cache('movies', film['_id'])
    redis_response = await redis_client.get(cache_key)
    redis_data = orjson.loads(redis_response)

    assert elastic_response.body['id'] == redis_data['_source']['id']
    assert elastic_response.body['title'] == redis_data['_source']['title']
    assert elastic_response.body['description'] == redis_data['_source']['description']
    assert elastic_response.body['imdb_rating'] == redis_data['_source']['imdb_rating']
    assert elastic_response.body['genres_list'] == redis_data['_source']['genres_list']
    assert elastic_response.body['directors_names'] == redis_data['_source']['directors_names']
    assert elastic_response.body['actors_names'] == redis_data['_source']['actors_names']
    assert elastic_response.body['writers_names'] == redis_data['_source']['writers_names']
