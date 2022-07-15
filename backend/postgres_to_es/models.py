"""
Датаклассы объектов для загрузки в ES.

"""

import uuid
from datetime import datetime
from typing import Any

from pydantic.dataclasses import dataclass


@dataclass
class BaseClass:
    id: uuid.UUID
    updated_at: datetime


@dataclass
class Film(BaseClass):
    rating: Any
    title: str
    description: Any
    created_at: datetime
    creation_date: Any
    type: str
    directors: list
    actors: list
    writers: list
    genres: list


@dataclass
class Genre(BaseClass):
    name: str
    descr: Any


@dataclass
class Person(BaseClass):
    name: str
