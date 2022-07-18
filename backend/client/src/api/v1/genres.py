from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from services.genre import GenreService

from .models import Genre

router = APIRouter(prefix='/api/v1/genres', tags=['Genres'])

@router.get(path='/{genre_id}', name='Genre Detail', response_model=Genre)
async def genre_details(genre_id: str, genre_service: GenreService = Depends(GenreService.get_service)) -> Genre:
    genre = await genre_service.get_by_id(id=genre_id)

    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Genre not found')

    return Genre(id=genre.id, name=genre.name)
