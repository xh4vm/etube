from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from services.genre import GenreService

from models.models import GenreModelBrief, GenreModel

router = APIRouter(prefix='/api/v1', tags=['Genres'])

@router.get(path='/genre/{genre_id}', name='Genre Detail', response_model=GenreModel)
async def genre_details(
        genre_id: str,
        genre_service: GenreService = Depends(GenreService.get_service),
) -> GenreModel:
    genre = await genre_service.get_by_id(id=genre_id)
    films = await genre_service.search(
        custom_index='movies',
        search_field='genre',
        search_value=genre.name,
    )
    film_titles = [film['title'] for film in films]
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Genre not found')

    return GenreModel(id=genre.id, name=genre.name, films=film_titles)


@router.get(path='/genres/', name='List of genres')
async def genres_list(
        page=1,
        page_size=10,
        value='',
        genre_service: GenreService = Depends(GenreService.get_service)) -> list:
    genres = await genre_service.search(page, page_size, value)
    return [GenreModelBrief(id=genre.id, name=genre.name) for genre in genres]
