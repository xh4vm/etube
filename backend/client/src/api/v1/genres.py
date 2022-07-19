from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException

from src.services.genre import GenreService
from src.services.giver import genre_service as giver_service
from src.models.models import GenreModelBrief, GenreModel


router = APIRouter(prefix='/genre', tags=['Genres'])


@router.get(path='/{genre_id}', name='Genre Detail', response_model=GenreModel)
async def genre_details(genre_id: str, genre_service: GenreService = Depends(giver_service)) -> GenreModel:
    genre = await genre_service.get_by_id(id=genre_id)
    films = await genre_service.search(
        custom_index='movies',
        search_fields=['genre'],
        search_value=genre.name,
    )
    film_titles = {film['title']: film['imdb_rating'] for film in films}
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Genre not found')

    return GenreModel(id=genre.id, name=genre.name, films=film_titles)


@router.get(path='s', name='List Of Genres', response_model=list[GenreModelBrief])
async def genres_list(
        page=1,
        page_size=10,
        search='',
        genre_service: GenreService = Depends(giver_service),
) -> list[GenreModelBrief]:
    search_fields = ['name', 'description']
    genres = await genre_service.search(page, page_size, search_fields, search)
    return [GenreModelBrief(id=genre.id, name=genre.name) for genre in genres]
