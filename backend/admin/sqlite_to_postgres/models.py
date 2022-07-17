"""
Датаклассы для валидации поступающих из sqlite данных.

Каждый датакласс и его атрибуты соответствуют таблицам
в БД postgres.
"""

import sqlite3
import uuid
from dataclasses import astuple, dataclass, field
from datetime import date

from logger import logger


@dataclass
class Base:
    """
    Базовый датакласс.

    Задает общие методы для составления sql запросов
    (метод получения атрибутов и метод получения значений объекта).
    """

    id: uuid.UUID

    @classmethod
    def get_slots(cls) -> str:
        """
        Возврат списка полей таблицы БД,
        готового для включения в query.
        """
        return ', '.join(tuple(cls.__dataclass_fields__))

    @classmethod
    def get_values(cls, d: sqlite3.Row) -> tuple:
        """
        Возврат кортежа данных, подходящего для загрузки в postgres,
        или None, если в словаре описаны не все атрибуты
        без дефолтных значений.
        """
        attrs = {}
        for k, v in dict(d).items():
            if k in cls.__dataclass_fields__:
                attrs[k] = v
        try:
            return astuple(cls(**attrs))
        except TypeError as error:
            logger.error(f'Ошибка создания объекта {d.get("id")}: {error}')


@dataclass
class FilmWork(Base):
    title: str
    description: str
    creation_date: date
    rating: float
    type: str
    created_at: str = field(default='NOW()')
    updated_at: str = field(default='NOW()')


@dataclass
class Person(Base):
    full_name: str
    created_at: str = field(default='NOW()')
    updated_at: str = field(default='NOW()')


@dataclass
class Genre(Base):
    name: str
    description: str
    created_at: str = field(default='NOW()')
    updated_at: str = field(default='NOW()')


@dataclass
class PersonFilmWork(Base):
    person_id: uuid.UUID
    film_work_id: uuid.UUID
    role: str
    created_at: str = field(default='NOW()')


@dataclass
class GenreFilmWork(Base):
    genre_id: uuid.UUID
    film_work_id: uuid.UUID
    created_at: str = field(default='NOW()')
