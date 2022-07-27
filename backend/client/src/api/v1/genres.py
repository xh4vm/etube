from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from src.core.config import CONFIG
from src.models.base import PageModel
from src.models.film import FilmModelBrief, FilmModelSort
from src.models.genre import GenreModelBrief, GenreModelFull
from src.services.film import FilmService
from src.services.genre import GenreService
from src.services.giver import film_service as other_giver_service
from src.services.giver import genre_service as giver_service

router = APIRouter(prefix='/genre', tags=['Genres'])


@router.get(path='/{genre_id}', name='Genre Detail', response_model=GenreModelFull)
async def genre_details(
    genre_id: str,
    film_service: FilmService = Depends(other_giver_service),
    genre_service: GenreService = Depends(giver_service),
) -> GenreModelFull:
    """Информация о жанре и топ {PAGE_SIZE} фильмов этого жанра"""

    genre = await genre_service.get_by_id(id=genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Genre not found')
    films: PageModel[FilmModelBrief] = await film_service.search(
        search_fields=['genre'], search_value=genre.name, sort_fields=FilmModelSort.IMDB_RATING_DESC.value,
    )

    return GenreModelFull(id=genre.id, name=genre.name, films=films.items)


@router.get(path='s', name='List Of Genres', response_model=PageModel[GenreModelBrief])
async def genres_list(
    page=CONFIG.APP.page,
    page_size=CONFIG.APP.page_size,
    search='',
    sort=None,
    genre_service: GenreService = Depends(giver_service),
) -> PageModel[GenreModelBrief]:
    return await genre_service.search(page=page, page_size=page_size, search_value=search, sort_fields=sort)
