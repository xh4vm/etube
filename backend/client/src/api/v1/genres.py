from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException

from src.models.models import GenreModel
from src.services.genre import GenreService, get_genre_service


router = APIRouter(prefix='/genres', tags=['Genres'])


@router.get(path='/{genre_id}', name='Genre Detail', response_model=GenreModel)
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_genre_service)) -> GenreModel:
    genre = await genre_service.get_by_id(id=genre_id)
    
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Genre not found')
    
    return genre
