from http import HTTPStatus

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from src.containers.person import ServiceContainer
from src.errors.person import PersonError
from src.models.base import PageModel, Paginator
from src.models.film import FilmModelBrief, FilmModelFull, FilmModelSort
from src.models.person import (PersonModelBrief, PersonModelFull,
                               PersonModelRole)
from src.services.film import FilmService
from src.services.person import PersonService

router = APIRouter(prefix='/person', tags=['Persons'])


@router.get(path='/{person_id}', name='Person Detail', response_model=PersonModelFull)
@inject
async def person_details(
    person_id: str,
    film_service: FilmService = Depends(Provide[ServiceContainer.film_service]),
    person_service: PersonService = Depends(Provide[ServiceContainer.person_service]),
) -> PersonModelFull:
    """Информация о персоне и топ {PAGE_SIZE} фильмов этого с участием этой персоны"""

    person: PersonModelFull = await person_service.get_by_id(id=person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=PersonError.NOT_FOUND)
    films: PageModel[FilmModelFull] = await film_service.search(
        search_fields=['directors_names', 'actors_names', 'writers_names'],
        search_value=person.name,
        sort_fields=FilmModelSort.IMDB_RATING_DESC.value,
        model_mapping=FilmModelFull,
    )

    person_films = {PersonModelRole.DIRECTOR: [], PersonModelRole.ACTOR: [], PersonModelRole.WRITER: []}
    for film in films.items:
        if person.name in film.directors_names:
            person_films[PersonModelRole.DIRECTOR].append(FilmModelBrief.parse_obj(film))
        if person.name in film.actors_names:
            person_films[PersonModelRole.ACTOR].append(FilmModelBrief.parse_obj(film))
        if person.name in film.writers_names:
            person_films[PersonModelRole.WRITER].append(FilmModelBrief.parse_obj(film))

    return PersonModelFull(id=person.id, name=person.name, films=person_films)


@router.get(path='s', name='List Of Persons', response_model=PageModel[PersonModelBrief])
@inject
async def persons_list(
    paginator: Paginator = Depends(),
    search='',
    sort=None,
    person_service: PersonService = Depends(Provide[ServiceContainer.person_service]),
) -> PageModel[PersonModelBrief]:
    return await person_service.search(
        page=paginator.page, page_size=paginator.page_size, search_value=search, sort_fields=sort
    )
