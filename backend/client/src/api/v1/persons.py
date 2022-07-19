from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from services.person import PersonService

from models.models import PersonModel, PersonModelBrief

router = APIRouter(prefix='/api/v1', tags=['Persons'])

@router.get(path='/person/{person_id}', name='Person Detail', response_model=PersonModel)
async def person_details(
        person_id: str,
        person_service: PersonService = Depends(PersonService.get_service),
) -> PersonModel:
    person = await person_service.get_by_id(id=person_id)
    films = await person_service.search(
        custom_index='movies',
        search_field='person',
        search_value=person.name,
    )
    film_titles = [film['title'] for film in films]
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Person not found')

    return PersonModel(id=person.id, name=person.name, films=film_titles)


@router.get(path='/persons/', name='List of persons')
async def persons_list(
        page=1,
        page_size=10,
        value='',
        person_service: PersonService = Depends(PersonService.get_service)) -> list:
    persons = await person_service.search(page, page_size, value)
    return [PersonModelBrief(id=person.id, name=person.name) for person in persons]
