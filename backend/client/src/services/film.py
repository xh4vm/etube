# from ..core.indices import FILM_INDEX
from models.models import FilmModel

from .base import BaseService


class FilmService(BaseService):
    index = 'movies'
    model = FilmModel


# class FilmService(BaseService):
#     index = FILM_INDEX.index
#     model = FILM_INDEX.model
#     search_fileds = FILM_INDEX.search_fields

