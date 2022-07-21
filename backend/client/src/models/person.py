from .base import ModelClass, StrEnum
from .film import FilmModelBrief


class PersonModelBrief(ModelClass):
    # Краткая версия модели для отображения при множественном поиске.
    # Является валидирующей для входящих из эластика данных.
    name: str


class PersonModelRole(StrEnum):
    DIRECTOR = 'director'
    ACTOR = 'actor'
    WRITER = 'writer'


class PersonModelFull(PersonModelBrief):
    # Полная версия модели для отображения при поиске одного человека.
    # Список фильмов в виде словаря, в котором ключи - роль человека в фильме.
    films: dict[PersonModelRole, list[FilmModelBrief]] = None


class PersonModelSort(StrEnum):
    NAME_ASC = 'name.raw'
    NAME_DESC = 'name.raw:desc'