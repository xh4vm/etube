from ..core.indices import FILM_INDEX
from .base import BaseService


class FilmService(BaseService):
    index = FILM_INDEX.index
    model = FILM_INDEX.model
    search_fileds = FILM_INDEX.search_fields
