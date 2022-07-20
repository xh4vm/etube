from ..core.indices import FILM_INDEX
from .base import BaseService


class FilmService(BaseService):
    index = FILM_INDEX.index
    brief_model = FILM_INDEX.brief_model
    full_model = FILM_INDEX.full_model
    search_fields = FILM_INDEX.search_fields
