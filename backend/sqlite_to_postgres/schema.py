from datetime import date, datetime
from typing import Optional
import uuid

from dataclasses import dataclass, field
from enforce_typing import enforce_types


SCHEMA_NAME = 'content'


class Schema:
    film_work = 'film_work'
    genre = 'genre'
    person = 'person'
    genre_film_work = 'genre_film_work'
    person_film_work = 'person_film_work'


@dataclass
class UUIDMixin:
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    class Meta:
        abstract = True


@dataclass
class TimeStampedMixin:
    created_at: Optional[datetime] = field(default=None)
    updated_at: Optional[datetime] = field(default=None)

    class Meta:
        abstract = True


@enforce_types
@dataclass
class FilmWorkBase:
    title: str
    description: Optional[str]
    file_path: Optional[str]
    type: str
    creation_date: Optional[date] = field(default=None)
    rating: Optional[float] = field(default=None)


@enforce_types
@dataclass
class FilmWork(UUIDMixin, TimeStampedMixin, FilmWorkBase):
    pass


@enforce_types
@dataclass
class GenreBase:
    name: str
    description: Optional[str]


@enforce_types
@dataclass
class Genre(UUIDMixin, TimeStampedMixin, GenreBase):
    pass


@enforce_types
@dataclass
class GenreFilmWorkBase:
    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created_at: datetime


@enforce_types
@dataclass
class GenreFilmWork(UUIDMixin, GenreFilmWorkBase):
    pass


@enforce_types
@dataclass
class PersonBase:
    full_name: str


@enforce_types
@dataclass
class Person(UUIDMixin, TimeStampedMixin, PersonBase):
    pass


@enforce_types
@dataclass
class PersonFilmWorkBase:
    film_work_id: uuid.UUID
    person_id: uuid.UUID
    role: str
    created_at: datetime


@enforce_types
@dataclass
class PersonFilmWork(UUIDMixin, PersonFilmWorkBase):
    pass
