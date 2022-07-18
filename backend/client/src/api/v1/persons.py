from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException

from src.services.person import PersonService
from src.services.giver import person_service as giver_service
from .models import Person


router = APIRouter(prefix='/person', tags=['Persons'])

@router.get(path='/{person_id}', name='Person Detail', response_model=Person)
async def person_details(person_id: str, person_service: PersonService = Depends(giver_service)) -> Person:
    person = await person_service.get_by_id(id=person_id)

    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Person not found')

    return Person(id=person.id, name=person.name)
