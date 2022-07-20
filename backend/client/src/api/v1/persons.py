from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException

from src.services.person import PersonService
from src.services.giver import person_service as giver_service
from src.models.models import PersonModelFull, PersonModelBrief


router = APIRouter(prefix='/person', tags=['Persons'])


@router.get(path='/{person_id}', name='Person Detail', response_model=PersonModelFull)
async def person_details(person_id: str, person_service: PersonService = Depends(giver_service)) -> PersonModelFull:
    person = await person_service.get_by_id(id=person_id)
    films = await person_service.search(
        custom_index='movies',
        search_fields=['director', 'actors_names', 'writers_names'],
        search_value=person.name,
    )

    person_films = {'director': [], 'actor': [], 'writer': []}
    for film in films:
        title = film['title']
        person_films['director'].append(title) if person.name in film['director'] else None
        person_films['actor'].append(title) if person.name in film['actors_names'] else None
        person_films['writer'].append(title) if person.name in film['writers_names'] else None

    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Person not found')

    return PersonModelFull(id=person.id, name=person.name, films=person_films)


@router.get(path='s', name='List Of Persons', response_model=list[PersonModelBrief])
async def persons_list(
        page=1,
        page_size=10,
        search='',
        person_service: PersonService = Depends(giver_service),
) -> list[PersonModelBrief]:
    search_fields = ['name']
    persons = await person_service.search(page, page_size, search_fields, search)
    return [PersonModelBrief(id=person.id, name=person.name) for person in persons]
