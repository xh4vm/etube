from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException

from src.services.base import BaseService
from src.services.film import FilmService
from src.services.giver import film_service as giver_service
from .models import Film


router = APIRouter(prefix='/film', tags=['Films'])

@router.get(path='/{film_id}', name='Film Detail', response_model=Film)
async def film_details(film_id: str, film_service: FilmService = Depends(giver_service)) -> Film:
    film = await film_service.get_by_id(id=film_id)

    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Film not found')

    return Film(id=film.id, title=film.title)


@router.get(path='s', name='Search Films', response_model=list[Film])
async def search_film(film_service: FilmService = Depends(giver_service)) -> Film:
    return []
