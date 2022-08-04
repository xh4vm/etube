import pytest


@pytest.mark.asyncio
async def test_film_search(generate_movies, make_get_request):
    # Проверка поиска фильма по точному совпадению названия (должен быть первым в списке).
    expected = generate_movies[0]
    film_id = expected['_id']
    film_title = expected['_source']['title']
    response = await make_get_request('films', params={'search': film_title})

    assert response.status == 200
    assert response.body['items'][0]['id'] == film_id


@pytest.mark.asyncio
async def test_pagination_page_size(generate_movies, make_get_request):
    # Проверка настройки количества документов на странице.
    PAGE_SIZE = 4
    response = await make_get_request('films', params={'page_size': PAGE_SIZE})

    assert len(response.body['items']) == PAGE_SIZE


@pytest.mark.asyncio
async def test_pagination_metadata_page_1(generate_movies, make_get_request):
    # Проверка мета-данных первой страницы.
    response = await make_get_request('films', params={'page': 1, 'page_size': 1, })

    assert response.body['prev_page'] is None
    assert response.body['next_page'] == 2
    assert response.body['total'] == len(generate_movies)
    assert len(response.body['items']) == 1


@pytest.mark.asyncio
async def test_pagination_metadata_page_2(generate_movies, make_get_request):
    # Проверка мета-данных второй страницы.
    response = await make_get_request('films', params={'page': 2, 'page_size': 1, })

    assert response.body['prev_page'] == 1
    assert response.body['next_page'] == 3
    assert response.body['total'] == len(generate_movies)
    assert len(response.body['items']) == 1
