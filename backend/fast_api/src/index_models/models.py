import orjson

from pydantic import BaseModel
from typing import Optional


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class ModelClass(BaseModel):
    id: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class FilmModel(ModelClass):
    title: str
    description: str


class GenreModel(ModelClass):
    name: str
    description: Optional[str]


class PersonModel(ModelClass):
    name: str
