from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException

from src.models.models import FilmModel
from src.services.film import FilmService, get_film_service


router = APIRouter(prefix='/films', tags=['Films'])


@router.get(path='/{film_id}', name='Film Detail', response_model=FilmModel)
async def film_details(film_id: str, film_service: FilmService = Depends(get_film_service)) -> FilmModel:
    film = await film_service.get_by_id(id=film_id)
    
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Film not found')
    
    return film
