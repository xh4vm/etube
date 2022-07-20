from typing import Optional

from .base import ModelClass, StrEnum


class GenreModelBrief(ModelClass):
    # Краткая версия модели для отображения при множественном поиске.
    # Является валидирующей для входящих из эластика данных.
    name: str


class GenreModelFull(GenreModelBrief):
    # Полная версия модели для отображения при поиске одного жанра.
    # Список фильмов в виде словаря {название: рейтинг}.
    description: Optional[str]
    films: dict = None


class GenreModelSort(StrEnum):
    NAME_ASC = 'name.raw'
    NAME_DESC = 'name.raw:desc'
