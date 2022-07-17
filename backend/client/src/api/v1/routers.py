from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from .models import Film, Genre, Person
from models.models import FilmModel, GenreModel, PersonModel

from services.base_service import get_service
from services.film import FilmService
from services.genre import GenreService
from services.person import PersonService

router = APIRouter()

@router.get('/film/{film_id}', response_model=Film)
async def film_details(film_id: str, film_service: FilmService = Depends(get_service)) -> Film:
    film = await film_service.get_by_id(film_id, 'movies', FilmModel)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')
    return Film(id=film.id, title=film.title)


@router.get('/genre/{genre_id}', response_model=Genre)
async def genre_details(genre_id: str, genre_service: GenreService = Depends(get_service)) -> Genre:
    genre = await genre_service.get_by_id(genre_id, 'genres', GenreModel)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')

    return Genre(id=genre.id, name=genre.name)


@router.get('/person/{person_id}', response_model=Person)
async def person_details(person_id: str, person_service: PersonService = Depends(get_service)) -> Person:
    person = await person_service.get_by_id(person_id, 'persons', PersonModel)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='person not found')

    return Person(id=person.id, name=person.name)
