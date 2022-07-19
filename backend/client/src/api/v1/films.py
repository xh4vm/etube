from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException

from src.services.film import FilmService
from src.services.giver import film_service as giver_service
from src.models.models import FilmModel, FilmModelBrief


router = APIRouter(prefix='', tags=['Films'])

@router.get(path='/film/{film_id}', name='Film Detail', response_model=FilmModel)
async def film_details(film_id: str, film_service: FilmService = Depends(giver_service)) -> FilmModel:
    film = await film_service.get_by_id(id=film_id)

    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Film not found')

    return FilmModel(id=film.id, title=film.title)


# @router.get(path='s', name='Search Films', response_model=list[Film])
# async def search_film(film_service: FilmService = Depends(giver_service)) -> Film:
#     return []


@router.get(path='/films/', name='List Of Films', response_model=list[FilmModelBrief])
async def films_list(
        page=1,
        page_size=10,
        value='',
        film_service: FilmService = Depends(giver_service),
) -> list[FilmModelBrief]:
    films = await film_service.search(page, page_size, value)
    return [FilmModelBrief(id=film.id, title=film.title) for film in films]
