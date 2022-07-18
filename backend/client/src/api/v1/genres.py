from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException

from src.services.genre import GenreService
from src.services.giver import genre_service as giver_service
from .models import Genre


router = APIRouter(prefix='/genre', tags=['Genres'])

@router.get(path='/{genre_id}', name='Genre Detail', response_model=Genre)
async def genre_details(genre_id: str, genre_service: GenreService = Depends(giver_service)) -> Genre:
    genre = await genre_service.get_by_id(id=genre_id)

    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Genre not found')

    return Genre(id=genre.id, name=genre.name)
