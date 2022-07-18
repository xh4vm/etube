from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException

from services.person import PersonService

from .models import Person

router = APIRouter(prefix='/api/v1/persons', tags=['Persons'])

@router.get(path='/{person_id}', name='Person Detail', response_model=Person)
async def person_details(person_id: str, person_service: PersonService = Depends(PersonService.get_service)) -> Person:
    person = await person_service.get_by_id(id=person_id)

    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Person not found')

    return Person(id=person.id, name=person.name)
