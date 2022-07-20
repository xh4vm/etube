from ..core.indices import PERSON_INDEX
from .base import BaseService


class PersonService(BaseService):
    index = PERSON_INDEX.index
    brief_model = PERSON_INDEX.brief_model
    full_model = PERSON_INDEX.full_model
    search_fields = PERSON_INDEX.search_fields
