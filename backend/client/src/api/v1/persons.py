from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from src.models.models import PersonModel

from src.services.person import PersonService, get_person_service


router = APIRouter(prefix='/persons', tags=['Persons'])

@router.get(path='/{person_id}', name='Person Detail', response_model=PersonModel)
async def person_details(person_id: str, person_service: PersonService = Depends(get_person_service)) -> PersonModel:
    person = await person_service.get_by_id(id=person_id)
    
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='Person not found')
    
    return person
