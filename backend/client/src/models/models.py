from typing import Optional

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class ModelClass(BaseModel):
    id: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class FilmModelBrief(ModelClass):
    # Краткая версия модели для отображения при множественном поиске.
    title: str


class FilmModel(FilmModelBrief):
    # Полная версия модели для отображения при поиске одного фильма.
    # Является валидирующей для входящих из эластика данных.
    description: str
    imdb_rating: Optional[float]
    director: list
    actors_names: list
    writers_names: list
    genre: list
    description: str = None


class GenreModelBrief(ModelClass):
    # Краткая версия модели для отображения при множественном поиске.
    # Является валидирующей для входящих из эластика данных.
    name: str


class GenreModel(GenreModelBrief):
    # Полная версия модели для отображения при поиске одного жанра.
    description: Optional[str]
    films: list = None


class PersonModelBrief(ModelClass):
    # Краткая версия модели для отображения при множественном поиске.
    # Является валидирующей для входящих из эластика данных.
    name: str


class PersonModel(PersonModelBrief):
    # Полная версия модели для отображения при поиске одного человека.
    films: list = None
