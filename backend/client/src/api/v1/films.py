from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from services.film import FilmService

from models.models import FilmModel, FilmModelBrief

router = APIRouter(prefix='/api/v1', tags=['Films'])

@router.get(path='/film/{film_id}', name='Film Detail', response_model=FilmModel)
async def film_details(film_id: str, film_service: FilmService = Depends(FilmService.get_service)) -> FilmModel:
    film = await film_service.get_by_id(id=film_id)

    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Film not found')

    return film

@router.get(path='/films/', name='List of Films')
async def films_list(
        page=1,
        page_size=10,
        value='',
        film_service: FilmService = Depends(FilmService.get_service)) -> list:
    films = await film_service.search(page, page_size, value)
    return [FilmModelBrief(id=film.id, title=film.title) for film in films]
