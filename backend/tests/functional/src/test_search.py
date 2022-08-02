import pytest


@pytest.mark.asyncio
async def test_film_search(redis_client, generate_docs, make_get_request):
    # Проверка поиска фильма по точному совпадению названия (должен быть первым в списке).
    await redis_client.flushall()
    film_for_test = generate_docs.films[0]['_source']
    film_id = film_for_test['id']
    film_title = film_for_test['title']
    response = await make_get_request(f'films?search={film_title}')

    assert response.status == 200
    assert response.body['items'][0]['id'] == film_id


@pytest.mark.asyncio
async def test_pagination_page_1(redis_client, make_get_request):
    # Проверка настройки количества документов на странице.
    PAGE_SIZE = 4
    await redis_client.flushall()
    response = await make_get_request(f'films?page_size={PAGE_SIZE}')

    assert len(response.body['items']) == PAGE_SIZE


@pytest.mark.asyncio
async def test_pagination_page_1(redis_client, make_get_request):
    # Проверка мета-данных первой страницы.
    await redis_client.flushall()
    response = await make_get_request(f'films?page=1')

    assert response.body['prev_page'] == None


@pytest.mark.asyncio
async def test_pagination_page_1(redis_client, make_get_request):
    # Проверка мета-данных второй страницы.
    await redis_client.flushall()
    response = await make_get_request(f'films?page=2')

    assert response.body['prev_page'] == 1
