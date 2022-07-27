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


class GenreForFilm(GenrePersonBase):
    name: str


class Genre(GenreForFilm):
    description: Optional[str]


class Person(GenrePersonBase):
    name: str


class Film(UUIDModelMixin, TimeStampedModelMixin):
    imdb_rating: Optional[float]
    title: str
    description: Optional[str]
    creation_date: Optional[date]
    type: str
    directors: list[Person]
    actors: list[Person]
    writers: list[Person]
    genres: list[GenreForFilm]

    def _get_list_of_objects(self, objs: list[Optional[dict]], key: str = 'name') -> Union[list[str], list]:
        # Метод разворачивания словарей с персонами/жанрами в массив имен.
        return [obj[key] for obj in objs] if objs is not None else []

    def _get_dict_of_objects(self, objs: list[Union[Person, GenreForFilm]]) -> Union[list[dict], list]:
        # Преобразование объекта Person или Genre в словарь по схеме индекса.
        return [obj.index_data() for obj in objs] if objs is not None else []

    def index_data(self) -> dict:
        obj_dict = self.dict()
        obj_dict['id'] = str(obj_dict['id'])
        obj_dict.pop('updated_at')
        obj_dict.pop('creation_date')
        obj_dict.pop('type')
        obj_dict['genres_list'] = self._get_list_of_objects(obj_dict['genres'])
        obj_dict['genres'] = self._get_dict_of_objects(self.genres)
        obj_dict['directors_names'] = self._get_list_of_objects(obj_dict['directors'])
        obj_dict['actors_names'] = self._get_list_of_objects(obj_dict['actors'])
        obj_dict['writers_names'] = self._get_list_of_objects(obj_dict['writers'])
        obj_dict['directors'] = self._get_dict_of_objects(self.directors)
        obj_dict['actors'] = self._get_dict_of_objects(self.actors)
        obj_dict['writers'] = self._get_dict_of_objects(self.writers)

        return obj_dict
