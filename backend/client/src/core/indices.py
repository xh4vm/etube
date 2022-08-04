from pydantic import Field
from pydantic.main import ModelMetaclass

from ..models.film import (FilmModelBrief, FilmModelFilter, FilmModelFull,
                           FilmModelSort)
from ..models.genre import (GenreModelBrief, GenreModelFilter, GenreModelFull,
                            GenreModelSort)
from ..models.person import (PersonModelBrief, PersonModelFilter,
                             PersonModelFull, PersonModelSort)
from .config import Settings


class FilmIndex(Settings):
    index: str = Field(..., env='INDEX_MOVIES')
    brief_model: ModelMetaclass = FilmModelBrief
    full_model: ModelMetaclass = FilmModelFull
    search_fields: list[str] = ['title^2', 'description']
    model_sort: ModelMetaclass = FilmModelSort
    model_filter: ModelMetaclass = FilmModelFilter


class GenreIndex(Settings):
    index: str = Field(..., env='INDEX_GENRES')
    brief_model: ModelMetaclass = GenreModelBrief
    full_model: ModelMetaclass = GenreModelFull
    search_fields: list[str] = ['name^2', 'description']
    model_sort: ModelMetaclass = GenreModelSort
    model_filter: ModelMetaclass = GenreModelFilter


class PersonIndex(Settings):
    index: str = Field(..., env='INDEX_PERSONS')
    brief_model: ModelMetaclass = PersonModelBrief
    full_model: ModelMetaclass = PersonModelFull
    search_fields: list[str] = ['name']
    model_sort: ModelMetaclass = PersonModelSort
    model_filter: ModelMetaclass = PersonModelFilter


FILM_INDEX = FilmIndex()
GENRE_INDEX = GenreIndex()
PERSON_INDEX = PersonIndex()
