import enum
import uuid
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel

SCHEMA = 'content'


class FilmWorkTypeEnum(str, enum.Enum):
    MOVIE = 'movie'
    TV_SHOW = 'tv_show'


class PersonFilmWorkRoleEnum(str, enum.Enum):
    ACTOR = 'actor'
    WRITER = 'writer'
    DIRECTOR = 'director'


class Schema:
    film_work = 'film_work'
    genre = 'genre'
    person = 'person'
    genre_film_work = 'genre_film_work'
    person_film_work = 'person_film_work'


class UUIDModelMixin(BaseModel):
    id: uuid.UUID


class TimeStampedModelMixin(BaseModel):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class GenreModel(UUIDModelMixin, TimeStampedModelMixin):
    name: str
    description: str

    class Meta:
        model = f'{SCHEMA}.{Schema.genre}'


class FilmWorkModel(UUIDModelMixin, TimeStampedModelMixin):
    title: str
    description: Optional[str] = None
    creation_date: Optional[date] = None
    file_path: Optional[str] = None
    rating: Optional[float] = None
    type: FilmWorkTypeEnum = FilmWorkTypeEnum.MOVIE

    class Meta:
        model = f'{SCHEMA}.{Schema.film_work}'


class GenreFilmWorkModel(UUIDModelMixin):
    film_work: FilmWorkModel
    genre: GenreModel
    created_at: Optional[datetime] = None

    class Meta:
        model = f'{SCHEMA}.{Schema.genre_film_work}'


class PersonModel(UUIDModelMixin, TimeStampedModelMixin):
    full_name: str

    class Meta:
        model = f'{SCHEMA}.{Schema.person}'


class PersonModelIntoES(UUIDModelMixin):
    name: str


class PersonFilmWorkModel(UUIDModelMixin, TimeStampedModelMixin):
    film_work: FilmWorkModel
    person: PersonModel
    role: PersonFilmWorkRoleEnum
    created_at: Optional[datetime] = None

    class Meta:
        model = f'{SCHEMA}.{Schema.person_film_work}'


class FilmWorkModelIntoES(UUIDModelMixin):
    title: str
    description: Optional[str] = None
    imdb_rating: Optional[float] = None
    genre: list[str] = []
    director: Optional[str] = None
    actors_names: list[str] = []
    writers_names: list[str] = []
    actors: list[PersonModelIntoES] = []
    writers: list[PersonModelIntoES] = []
