from pydantic import Field
from pydantic.main import ModelMetaclass

from ..models.models import FilmModel, GenreModelBrief, PersonModelBrief
from .config import Settings


class FilmIndex(Settings):
    index: str = Field(..., env='INDEX_MOVIES')
    model: ModelMetaclass = FilmModel
    search_fields: list[str] = ['title', 'description']


class GenreIndex(Settings):
    index: str = Field(..., env='INDEX_GENRES')
    model: ModelMetaclass = GenreModelBrief
    search_fields: list[str] = ['name', 'description']


class PersonIndex(Settings):
    index: str = Field(..., env='INDEX_PERSONS')
    model: ModelMetaclass = PersonModelBrief
    search_fields: list[str] = ['name']


FILM_INDEX = FilmIndex()
GENRE_INDEX = GenreIndex()
PERSON_INDEX = PersonIndex()
