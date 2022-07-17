from datetime import date, datetime
from typing import Optional
import uuid
from schema import Genre, Person, FilmWork, GenreFilmWork, PersonFilmWork
from enums import FilmWorkType, PersonFilmWorkRole
import logging

from dateutil.parser import parse


class Handler:
    def __init__(
        self,
        id: Optional[uuid.UUID],
        created_at: Optional[datetime.isoformat] = None,
        updated_at: Optional[datetime.isoformat] = None,
    ):
        self.id = uuid.UUID(id) if isinstance(id, str) else id
        self.created_at = parse(created_at) if isinstance(created_at, str) else created_at
        self.updated_at = parse(updated_at) if isinstance(updated_at, str) else updated_at
        self.logger = logging.getLogger(__name__)


class GenreHandler(Handler):
    def __init__(self, name: str, description: str, *args, **kwargs) -> None:
        self.name = name
        self.description = description

        super().__init__(*args, **kwargs)

    def get_dataclass(self) -> Optional[Genre]:

        if self.id is None:
            self.logger.debug(f'Genre id is none. Getting next element.')
            return None

        return Genre(
            name=self.name,
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at,
            id=self.id,
        )


class PersonHandler(Handler):
    def __init__(self, full_name: str, *args, **kwargs) -> None:
        self.full_name = full_name

        super().__init__(*args, **kwargs)

    def get_dataclass(self) -> Optional[Person]:

        if self.id is None:
            self.logger.debug(f'Person id is none. Getting next element.')
            return None

        return Person(full_name=self.full_name, created_at=self.created_at, updated_at=self.updated_at, id=self.id)


class FilmWorkHandler(Handler):
    def __init__(
        self,
        title: Optional[str],
        description: Optional[str],
        creation_date: Optional[date],
        file_path: Optional[str],
        rating: Optional[float],
        type: Optional[str],
        *args,
        **kwargs,
    ) -> None:
        self.title = title
        self.description = description
        self.creation_date = creation_date
        self.file_path = file_path
        self.rating = rating
        self.type = FilmWorkType.find_element(type).value

        super().__init__(*args, **kwargs)

    def get_dataclass(self) -> Optional[FilmWork]:

        if self.id is None:
            self.logger.debug(f'FilmWork id is none. Getting next element.')
            return None

        return FilmWork(
            title=self.title,
            description=self.description,
            creation_date=self.creation_date,
            file_path=self.file_path,
            rating=self.rating,
            type=self.type,
            created_at=self.created_at,
            updated_at=self.updated_at,
            id=self.id,
        )


class GenreFilmWorkHandler(Handler):
    def __init__(self, film_work_id: Optional[uuid.UUID], genre_id: Optional[uuid.UUID], *args, **kwargs) -> None:
        self.film_work_id = uuid.UUID(film_work_id) if isinstance(film_work_id, str) else film_work_id
        self.genre_id = uuid.UUID(genre_id) if isinstance(genre_id, str) else genre_id

        super().__init__(*args, **kwargs)

    def get_dataclass(self) -> Optional[Genre]:

        if self.id is None:
            self.logger.debug(f'GenreFilmWork id is none. Getting next element.')
            return None

        return GenreFilmWork(
            film_work_id=self.film_work_id, genre_id=self.genre_id, created_at=self.created_at, id=self.id,
        )


class PersonFilmWorkHandler(Handler):
    def __init__(
        self, film_work_id: Optional[uuid.UUID], person_id: Optional[uuid.UUID], role: Optional[str], *args, **kwargs
    ) -> None:
        self.film_work_id = uuid.UUID(film_work_id) if isinstance(film_work_id, str) else film_work_id
        self.person_id = uuid.UUID(person_id) if isinstance(person_id, str) else person_id
        self.role = PersonFilmWorkRole.find_element(role).value if isinstance(role, str) else role

        super().__init__(*args, **kwargs)

    def get_dataclass(self) -> Optional[Person]:

        if self.id is None:
            self.logger.debug(f'PersonFilmWork id is none. Getting next element.')
            return None

        return PersonFilmWork(
            film_work_id=self.film_work_id,
            person_id=self.person_id,
            role=self.role,
            created_at=self.created_at,
            id=self.id,
        )
