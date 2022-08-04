import random
from typing import Any, Literal
from pydantic import BaseModel, Field

from .base import fake, get_new_id
from .genre import FakeGenreBrief, FakeGenreFull
from .person import FakePersonBrief, FakePersonFull
    

class FakeFilmBrief(BaseModel):
    id: str = Field(default_factory=get_new_id)
    title: str = Field(default_factory=fake.sentence)
    imdb_rating: float = Field(default_factory=lambda: round(random.randrange(10, 100) / 10, 1))    


class FakeFilmFull(FakeFilmBrief):
    description: str = Field(default_factory=fake.text)
    genres: list[FakeGenreBrief] = Field(default=[])
    directors: list[FakePersonBrief] = Field(default=[])
    actors: list[FakePersonBrief] = Field(default=[])
    writers: list[FakePersonBrief] = Field(default=[]) 
    genres_list: list[str] = Field(default=[]) 
    directors_names: list[str] = Field(default=[]) 
    actors_names: list[str] = Field(default=[]) 
    writers_names: list[str] = Field(default=[]) 

    def __init__(self, **data: dict[str, Any]):
        data['genres_list'] = [model['name'] for model in data['genres']]
        data['directors_names'] = [model['name'] for model in data['directors']]
        data['actors_names'] = [model['name'] for model in data['actors']]
        data['writers_names'] = [model['name'] for model in data['writers']]
        super().__init__(**data)


class FakeFilmGenreRel(FakeGenreFull):
    films: list[FakeFilmBrief] = Field(default=[])


class FakeFilmPersonRel(FakePersonFull):
    films: dict[Literal['actor', 'writer', 'director'], list[FakeFilmBrief]] = Field(default={'actor': [], 'writer': [], 'director': []})
