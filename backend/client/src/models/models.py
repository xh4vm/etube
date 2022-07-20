import enum
import orjson
from typing import Optional, Generic, TypeVar
from pydantic import BaseModel, Field


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class JSONModel(BaseModel):
    
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class ModelClass(JSONModel):
    id: str


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


class FilmModelSort(str, enum.Enum):
    TITLE_ASC = 'title.raw'
    TITLE_DESC = '-title.raw'
    IMDB_RATING_ASC = 'imdb_rating'
    IMDB_RATING_DESC = '-imdb_rating'


class GenreModelBrief(ModelClass):
    # Краткая версия модели для отображения при множественном поиске.
    # Является валидирующей для входящих из эластика данных.
    name: str


class GenreModelFull(GenreModelBrief):
    # Полная версия модели для отображения при поиске одного жанра.
    # Список фильмов в виде словаря {название: рейтинг}.
    description: Optional[str]
    films: dict = None


class PersonModelBrief(ModelClass):
    # Краткая версия модели для отображения при множественном поиске.
    # Является валидирующей для входящих из эластика данных.
    name: str


class PersonModelFull(PersonModelBrief):
    # Полная версия модели для отображения при поиске одного человека.
    # Список фильмов в виде словаря, в котором ключи - роль человека в фильме.
    films: dict = None


PTYPE = TypeVar('PTYPE')


class PageModel(JSONModel, Generic[PTYPE]):

    next_page: Optional[int] = Field(
        title='Номер следующей страницы', example=3
    )
    prev_page: Optional[int] = Field(
        title='Номер предыдущей страницы', example=1
    )
    page: Optional[int] = Field(
        default=1, title='Номер текущей страницы', example=2
    )
    page_size: Optional[int] = Field(
        default=50, title='Длина выборки', example=2
    )
    total: Optional[int] = Field(
        default=0, title='Общая мощность выборки', example=1000
    )
    items: list[PTYPE] = Field(
        default=[], title='Список объектов', example=[]
    )
