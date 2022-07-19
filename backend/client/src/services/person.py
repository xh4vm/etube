from ..core.indices import PERSON_INDEX
from .base import BaseService


class PersonService(BaseService):
    index = PERSON_INDEX.index
    model = PERSON_INDEX.model
    search_fields = PERSON_INDEX.search_fields
