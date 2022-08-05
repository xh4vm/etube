from http import HTTPStatus

import orjson
import pytest

from ..settings import CacheSettings
from ..utils.fake_models.person import FakePersonBrief

pytestmark = pytest.mark.asyncio


async def test_person_details(generate_movies, generate_persons, make_get_request):
    # Проверка поиска персоны по id (ответ 200 и полнота основных данных).
    expected = generate_persons[0]
    response = await make_get_request(f'person/{expected["_id"]}')

    assert response.status == HTTPStatus.OK
    assert response.body['id'] == expected['_source']['id']
    assert response.body['name'] == expected['_source']['name']
    assert response.body['films'] == expected['_source']['films']


async def test_person_error(make_get_request):
    # Поиск несуществующего человека.
    person_id = '0123456789'
    response = await make_get_request(f'person/{person_id}')

    assert response.status == HTTPStatus.NOT_FOUND


async def test_person_sort_name_desc(generate_persons, make_get_request):
    # Проверка правильности сортировки.
    expected_full_map = sorted(generate_persons, key=lambda elem: elem['_source']['name'], reverse=True)
    expected = [FakePersonBrief.parse_obj(person['_source']) for person in expected_full_map]

    response = await make_get_request('persons', params={'sort': 'name.raw:desc'})

    assert expected == response.body['items']


async def test_person_sort_name_asc(generate_persons, make_get_request):
    # Проверка правильности сортировки.
    expected_full_map = sorted(generate_persons, key=lambda elem: elem['_source']['name'])
    expected = [FakePersonBrief.parse_obj(person['_source']) for person in expected_full_map]

    response = await make_get_request('persons', params={'sort': 'name.raw'})

    assert expected == response.body['items']


async def test_person_cache(redis_client, generate_persons, make_get_request):
    # Проверка работы системы кэширования.
    person = generate_persons[1]

    elastic_response = await make_get_request(f'person/{person["_id"]}')
    elastic_data = elastic_response.body

    cache_key = CacheSettings.get_doc_id_cache('persons', person['_id'])
    redis_response = await redis_client.get(cache_key)
    redis_data = orjson.loads(redis_response)

    assert elastic_data['id'] == redis_data['_source']['id']
    assert elastic_data['name'] == redis_data['_source']['name']
