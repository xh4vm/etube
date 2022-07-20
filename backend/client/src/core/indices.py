from pydantic import Field
from pydantic.main import ModelMetaclass

from ..models.film import FilmModelBrief, FilmModelFull, FilmModelSort
from ..models.genre import GenreModelBrief, GenreModelFull, GenreModelSort
from ..models.person import PersonModelBrief, PersonModelFull, PersonModelSort
from .config import Settings


class FilmIndex(Settings):
    index: str = Field(..., env='INDEX_MOVIES')
    brief_model: ModelMetaclass = FilmModelBrief
    full_model: ModelMetaclass = FilmModelFull
    search_fields: list[str] = ['title', 'description']
    model_sort: ModelMetaclass = FilmModelSort


class GenreIndex(Settings):
    index: str = Field(..., env='INDEX_GENRES')
    brief_model: ModelMetaclass = GenreModelBrief
    full_model: ModelMetaclass = GenreModelFull
    search_fields: list[str] = ['name', 'description']
    model_sort: ModelMetaclass = GenreModelSort


class PersonIndex(Settings):
    index: str = Field(..., env='INDEX_PERSONS')
    brief_model: ModelMetaclass = PersonModelBrief
    full_model: ModelMetaclass = PersonModelFull
    search_fields: list[str] = ['name']
    model_sort: ModelMetaclass = PersonModelSort


FILM_INDEX = FilmIndex()
GENRE_INDEX = GenreIndex()
PERSON_INDEX = PersonIndex()
