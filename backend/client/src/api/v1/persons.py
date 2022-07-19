from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException

from src.services.person import PersonService
from src.services.giver import person_service as giver_service
from src.models.models import PersonModel, PersonModelBrief


router = APIRouter(prefix='', tags=['Persons'])

@router.get(path='/person/{person_id}', name='Person Detail', response_model=PersonModel)
async def person_details(person_id: str, person_service: PersonService = Depends(giver_service)) -> PersonModel:
    person = await person_service.get_by_id(id=person_id)

    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Person not found')

    return PersonModel(id=person.id, name=person.name)

@router.get(path='/persons/', name='List Of Persons', response_model=list[PersonModelBrief])
async def persons_list(
        page=1,
        page_size=10,
        value='',
        person_service: PersonService = Depends(giver_service),
) -> list[PersonModelBrief]:
    persons = await person_service.search(page, page_size, value)
    return [PersonModelBrief(id=person.id, name=person.name) for person in persons]
