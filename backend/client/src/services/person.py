# from ..core.indices import PERSON_INDEX
from models.models import PersonModel

from .base import BaseService


class PersonService(BaseService):
    index = 'persons'
    model = PersonModel

# class PersonService(BaseService):
#     index = PERSON_INDEX.index
#     model = PERSON_INDEX.model
#     search_fileds = PERSON_INDEX.search_fields
