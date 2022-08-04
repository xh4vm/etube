import orjson
import pytest
from ..settings import CacheSettings


@pytest.mark.asyncio
async def test_person_details(generate_movies, generate_persons, make_get_request):
    # Проверка поиска персоны по id (ответ 200 и полнота основных данных).
    expected = generate_persons[0]
    response = await make_get_request(f'person/{expected["_id"]}')

    assert response.status == 200
    assert response.body['id'] == expected['_source']['id']
    assert response.body['name'] == expected['_source']['name']
    assert response.body['films'] == expected['_source']['films']


@pytest.mark.asyncio
async def test_person_error(make_get_request):
    # Поиск несуществующего человека.
    person_id = '0123456789'
    response = await make_get_request(f'person/{person_id}')

    assert response.status == 404


@pytest.mark.asyncio
async def test_person_sort(make_get_request):
    # Проверка правильности сортировки.
    response = await make_get_request(f'persons?sort=name.raw')
    persons_in_response = [person['name'] for person in response.body['items']]

    assert persons_in_response == sorted(persons_in_response)


@pytest.mark.asyncio
async def test_person_cache(redis_client, generate_persons, make_get_request):
    # Проверка работы системы кэширования.
    person = generate_persons[1]

    elastic_response = await make_get_request(f'person/{person["_id"]}')
    elastic_data = elastic_response.body

    cache_key = CacheSettings.get_doc_id_cache('persons', person["_id"])
    redis_response = await redis_client.get(cache_key)
    redis_data = orjson.loads(redis_response)

    assert elastic_data['id'] == redis_data['_source']['id']
    assert elastic_data['name'] == redis_data['_source']['name']
