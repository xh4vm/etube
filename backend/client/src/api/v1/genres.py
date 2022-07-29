from http import HTTPStatus
from dependency_injector.wiring import inject, Provide

from fastapi import APIRouter, Depends, HTTPException
from src.core.config import CONFIG
from src.models.base import PageModel
from src.models.film import FilmModelBrief, FilmModelSort
from src.models.genre import GenreModelBrief, GenreModelFull
from src.services.film import FilmService
from src.services.genre import GenreService
from src.containers.genre import ServiceContainer

router = APIRouter(prefix='/genre', tags=['Genres'])


@router.get(path='/{genre_id}', name='Genre Detail', response_model=GenreModelFull)
@inject
async def genre_details(
    genre_id: str,
    film_service: FilmService = Depends(Provide[ServiceContainer.film_service]),
    genre_service: GenreService = Depends(Provide[ServiceContainer.genre_service])
) -> GenreModelFull:
    """Информация о жанре и топ {PAGE_SIZE} фильмов этого жанра"""

    genre = await genre_service.get_by_id(id=genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Genre not found')
    films: PageModel[FilmModelBrief] = await film_service.search(
        search_fields=['genres_list'], search_value=genre.name, sort_fields=FilmModelSort.IMDB_RATING_DESC.value,
    )

    return GenreModelFull(id=genre.id, name=genre.name, films=films.items)


@router.get(path='s', name='List Of Genres', response_model=PageModel[GenreModelBrief])
@inject
async def genres_list(
    page=CONFIG.APP.page,
    page_size=CONFIG.APP.page_size,
    search='',
    sort=None,
    genre_service: GenreService = Depends(Provide[ServiceContainer.genre_service])
) -> PageModel[GenreModelBrief]:
    return await genre_service.search(page=page, page_size=page_size, search_value=search, sort_fields=sort)
