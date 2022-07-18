from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from services.film import FilmService

from .models import Film

router = APIRouter(prefix='/api/v1/films', tags=['Films'])

@router.get(path='/{film_id}', name='Film Detail', response_model=Film)
async def film_details(film_id: str, film_service: FilmService = Depends(FilmService.get_service)) -> Film:
    film = await film_service.get_by_id(id=film_id)

    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Film not found')

    return Film(id=film.id, title=film.title)
