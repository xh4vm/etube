from pydantic import Field
from pydantic.main import ModelMetaclass

from .config import Settings
from ..models.models import FilmModel, GenreModel, PersonModel


class FilmIndex(Settings):
    index: str = Field(..., env='INDEX_MOVIES')
    model: ModelMetaclass = FilmModel
    search_fields: list[str] = ['title', 'description']


class GenreIndex(Settings):
    index: str = Field(..., env='INDEX_GENRES')
    model: ModelMetaclass = GenreModel
    search_fields: list[str] = ['name', 'description']


class PersonIndex(Settings):
    index: str = Field(..., env='INDEX_PERSONS')
    model: ModelMetaclass = PersonModel
    search_fields: list[str] = ['name']


FILM_INDEX = FilmIndex()
GENRE_INDEX = GenreIndex()
PERSON_INDEX = PersonIndex()
