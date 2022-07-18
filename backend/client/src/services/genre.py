# from ..core.indices import GENRE_INDEX
from models.models import GenreModel

from .base import BaseService


class GenreService(BaseService):
    index = 'genres'
    model = GenreModel

# class GenreService(BaseService):
#     index = GENRE_INDEX.index
#     model = GENRE_INDEX.model
#     search_fileds = GENRE_INDEX.search_fields
