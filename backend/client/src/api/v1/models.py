from pydantic import BaseModel
from typing import Optional

class Film(BaseModel):
    id: str
    title: str
    imdb_rating: Optional[float]


class Genre(BaseModel):
    id: str
    name: str


class Person(BaseModel):
    id: str
    name: str
