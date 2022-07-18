from typing import Optional
from pydantic import BaseModel


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
