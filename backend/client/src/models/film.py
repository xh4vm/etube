from typing import Optional

from .base import ModelClass, StrEnum


class FilmModelBrief(ModelClass):
    # Краткая версия модели для отображения при множественном поиске.
    title: str
    imdb_rating: Optional[float]


class FilmModelFull(FilmModelBrief):
    # Полная версия модели для отображения при поиске одного фильма.
    # Является валидирующей для входящих из эластика данных.
    director: list[str]
    actors_names: list[str]
    writers_names: list[str]
    genre: list[str]
    description: str = None


class FilmModelSort(StrEnum):
    # Модель возможных параметров сортировки фильмов.
    TITLE_ASC = 'title.raw'
    TITLE_DESC = 'title.raw:desc'
    IMDB_RATING_ASC = 'imdb_rating'
    IMDB_RATING_DESC = 'imdb_rating:desc'


class FilmModelFilter(StrEnum):
    # Модель возможных параметров фильтрации фильмов.
    GENRE = 'genre'
