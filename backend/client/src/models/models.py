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


class FilmModel(ModelClass):
    title: str
    description: str
    imdb_rating: Optional[float]


class GenreModel(ModelClass):
    name: str
    description: Optional[str]


class PersonModel(ModelClass):
    name: str
