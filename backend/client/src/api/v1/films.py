from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException

from src.services.film import FilmService
from src.services.giver import film_service as giver_service
from src.models.models import FilmModel, FilmModelBrief


router = APIRouter(prefix='/film', tags=['Films'])


@router.get(path='/{film_id}', name='Film Detail', response_model=FilmModel)
async def film_details(film_id: str, film_service: FilmService = Depends(giver_service)) -> FilmModel:
    film = await film_service.get_by_id(id=film_id)

    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Film not found')

    return film


@router.get(path='s', name='List Of Films', response_model=list[FilmModelBrief])
async def films_list(
        page=1,
        page_size=10,
        search='',
        film_service: FilmService = Depends(giver_service),
) -> list[FilmModelBrief]:
    search_fields = ['title', 'description']
    films = await film_service.search(page, page_size, search_fields, search)
    return films
