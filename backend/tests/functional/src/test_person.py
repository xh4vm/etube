import orjson
import pytest


@pytest.mark.asyncio
async def test_person_details(redis_client, generate_docs, make_get_request):
    # Проверка поиска персоны по id (ответ 200 и полнота основных данных).
    await redis_client.flushall()
    person_for_test = generate_docs.persons[0]
    person_id = person_for_test['_id']
    main_fields = ['id', 'name']
    response = await make_get_request(f'person/{person_id}')

    assert response.status == 200

    for field in main_fields:
        assert response.body[field] == person_for_test['_source'][field]


@pytest.mark.asyncio
async def test_person_films_list(redis_client, generate_docs, make_get_request):
    # Выборочная проверка поля "Фильмы" при поиске жанра.
    await redis_client.flushall()
    # Берем режиссера из первого фильма, чтобы избежать ситуации,
    # когда выбрали персону без единого фильма.
    person_for_test = generate_docs.films[0]['_source']['directors'][0]
    films_with_person = generate_docs.films_with_person
    person_id = person_for_test['id']
    response = await make_get_request(f'person/{person_id}')
    person_films = response.body['films']
    # Проходим по каждой роли (режиссер, актер, сценарист)
    # и сравниваем список фильмов в ответе на запрос со списком в тестовых данных.
    print('***', person_films)
    print('***', films_with_person)
    for role, films in person_films.items():
        for film in films_with_person[role]:
            films.remove(film)

        assert films == []


@pytest.mark.asyncio
async def test_person_error(redis_client, make_get_request):
    # Поиск несуществующего жанра.
    await redis_client.flushall()
    person_id = '0123456789'
    response = await make_get_request(f'person/{person_id}')

    assert response.status == 404


@pytest.mark.asyncio
async def test_person_sort(redis_client, make_get_request):
    # Проверка правильности сортировки.
    await redis_client.flushall()
    response = await make_get_request(f'persons?sort=name.raw')
    persons_in_response = [person['name'] for person in response.body['items']]

    assert persons_in_response == sorted(persons_in_response)


@pytest.mark.asyncio
async def test_person_cache(redis_client, generate_docs, make_get_request):
    # Проверка работы системы кэширования.
    await redis_client.flushall()
    person_for_test = generate_docs.persons[0]
    person_id = person_for_test['_id']
    elastic_response = await make_get_request(f'person/{person_id}')
    cache_key = f'persons::detail::{person_id}'
    redis_response = await redis_client.get(cache_key)
    elastic_data = elastic_response.body
    redis_data = orjson.loads(redis_response)['_source']
    main_fields = ['id', 'name']
    for field in main_fields:
        assert redis_data[field] == elastic_data[field]
