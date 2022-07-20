from ..core.indices import GENRE_INDEX
from .base import BaseService


class GenreService(BaseService):
    index = GENRE_INDEX.index
    brief_model = GENRE_INDEX.brief_model
    full_model = GENRE_INDEX.full_model
    search_fields = GENRE_INDEX.search_fields
