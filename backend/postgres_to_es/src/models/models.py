"""
Валидация данных перед загрузкой в ES.

"""

import uuid
from datetime import date, datetime
from typing import Optional, Union

from pydantic import BaseModel


class UUIDModelMixin(BaseModel):
    id: uuid.UUID


class TimeStampedModelMixin(BaseModel):
    updated_at: Optional[datetime] = None


class GenrePersonBase(UUIDModelMixin, TimeStampedModelMixin):
    # Базовый класс для персон и жанров с обшим методом преобразования данных в словарь.
    def index_data(self):
        obj_dict = self.dict()
        obj_dict['id'] = str(obj_dict['id'])
        obj_dict.pop('updated_at')
        return obj_dict


class Genre(GenrePersonBase):
    name: str
    description: Optional[str]


class Person(GenrePersonBase):
    name: str


class Film(UUIDModelMixin, TimeStampedModelMixin):
    imdb_rating: Optional[float]
    title: str
    description: Optional[str]
    creation_date: Optional[date]
    type: str
    director: list[Person]
    actors: list[Person]
    writers: list[Person]
    genre: list

    def _get_short_persons(self, persons: list[Optional[dict]]) -> Union[list[str], list]:
        # Метод разворачивания словарей с персонами в массив имен.
        return [person['name'] for person in persons] if persons is not None else []

    def _get_persons_dict(self, persons: list[Optional[Person]]) -> Union[list[dict], list]:
        # Преобразование объекта Person в словарь по схеме индекса.
        return [person.index_data() for person in persons] if persons is not None else []

    def index_data(self) -> dict:
        obj_dict = self.dict()
        obj_dict['id'] = str(obj_dict['id'])
        obj_dict.pop('updated_at')
        obj_dict.pop('creation_date')
        obj_dict.pop('type')
        obj_dict['director'] = self._get_short_persons(obj_dict['director'])
        obj_dict['actors_names'] = self._get_short_persons(obj_dict['actors'])
        obj_dict['writers_names'] = self._get_short_persons(obj_dict['writers'])
        obj_dict['actors'] = self._get_persons_dict(self.actors)
        obj_dict['writers'] = self._get_persons_dict(self.writers)

        return obj_dict
