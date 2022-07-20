from pydantic import Field
from pydantic.main import ModelMetaclass

from ..models.models import (FilmModelBrief, FilmModelFull, GenreModelBrief, GenreModelFull,
                             PersonModelBrief, PersonModelFull)
from .config import Settings


class FilmIndex(Settings):
    index: str = Field(..., env='INDEX_MOVIES')
    brief_model: ModelMetaclass = FilmModelBrief
    full_model: ModelMetaclass = FilmModelFull
    search_fields: list[str] = ['title', 'description']


class GenreIndex(Settings):
    index: str = Field(..., env='INDEX_GENRES')
    brief_model: ModelMetaclass = GenreModelBrief
    full_model: ModelMetaclass = GenreModelFull
    search_fields: list[str] = ['name', 'description']


class PersonIndex(Settings):
    index: str = Field(..., env='INDEX_PERSONS')
    brief_model: ModelMetaclass = PersonModelBrief
    full_model: ModelMetaclass = PersonModelFull
    search_fields: list[str] = ['name']


FILM_INDEX = FilmIndex()
GENRE_INDEX = GenreIndex()
PERSON_INDEX = PersonIndex()
