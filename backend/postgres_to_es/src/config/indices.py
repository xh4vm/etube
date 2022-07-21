# Классы, определяющие параметры переноса данных
# из Postgres в ES, включая названия индексов.

from pydantic import Field

from ..etl.extractor import (FilmsPostgresExtractor, GenresPostgresExtracor,
                             PersonsPostgresExtractor)
from ..models.models import Film, Genre, Person
from .config import Settings


class FilmIndex(Settings):
    extractor = FilmsPostgresExtractor
    model = Film
    index: str = Field(..., env='INDEX_MOVIES')


class GenreIndex(Settings):
    extractor = GenresPostgresExtracor
    model = Genre
    index: str = Field(..., env='INDEX_GENRES')


class PersonIndex(Settings):
    extractor = PersonsPostgresExtractor
    model = Person
    index: str = Field(..., env='INDEX_PERSONS')


FILM_INDEX = FilmIndex()
GENRE_INDEX = GenreIndex()
PERSON_INDEX = PersonIndex()
