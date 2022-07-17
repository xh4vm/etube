from pydantic import BaseModel

class Film(BaseModel):
    id: str
    title: str


class Genre(BaseModel):
    id: str
    name: str


class Person(BaseModel):
    id: str
    name: str
