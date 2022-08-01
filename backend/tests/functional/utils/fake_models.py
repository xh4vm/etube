"""
Модели фейковых документов.

"""

import random
from typing import Any
import uuid

from faker import Faker

from pydantic import BaseModel, Field

fake = Faker()


def get_new_id() -> str:
    return str(uuid.uuid4())


class FakePerson(BaseModel):
    id: str = Field(default_factory=get_new_id)
    name: str = Field(default_factory=lambda: fake.name() + '::test::')


class FakeGenre(BaseModel):
    id: str = Field(default_factory=get_new_id)
    description: str = Field(default_factory=fake.text)
    name: str = Field(default_factory=lambda: fake.name() + '::test::')
    

class FakeFilm(BaseModel):
    id: str = Field(default_factory=get_new_id)
    title: str = Field(default_factory=lambda: fake.sentence() + '::test::')
    imdb_rating: float = Field(default_factory=lambda: round(random.randrange(10, 100) / 10, 1))
    description: str = Field(default_factory=fake.text)
    genres_list: list[str] = Field(default=[])
    directors_names: list[str] = Field(default=[])
    actors_names: list[str] = Field(default=[])
    writers_names: list[str] = Field(default=[]) 

    @property
    def genres(self) -> dict[str, Any]:
        return [FakeGenre(name=name) for name in self.genres_list]

    @property
    def directors(self) -> dict[str, Any]:
        return [FakePerson(name=name) for name in self.directors_names]

    @property
    def actors(self) -> dict[str, Any]:
        return [FakePerson(name=name) for name in self.actors_names]

    @property
    def writers(self) -> dict[str, Any]:
        return [FakePerson(name=name) for name in self.writers_names]
