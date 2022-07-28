"""
Модели фейковых документов.

"""

import random
import uuid
from faker import Faker


fake = Faker()


class FakePerson:

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.name = fake.name()


class FakeGenre:

    def __init__(self, name):
        self.id = str(uuid.uuid4())
        self.description = None
        self.name = name


class FakeFilm:

    def __init__(self, persons: list, genres: list):
        director = random.choice(persons)
        actors = [random.choice(persons) for _ in range(random.randint(2, 4))]
        writers = [random.choice(persons) for _ in range(random.randint(1, 2))]
        genres = [random.choice(genres) for _ in range(random.randint(1, 3))]

        self.id = str(uuid.uuid4())
        self.title = fake.sentence()
        self.imdb_rating = round(random.randrange(10, 100) / 10, 1)
        self.description = fake.sentence()
        self.directors_names = [director.name]
        self.actors_names = [actor.name for actor in actors]
        self.writers_names = [writer.name for writer in writers]
        self.genres_list = [genre.name for genre in genres]
        self.directors = [director.__dict__]
        self.genres = [{'id': genre.id, 'name': genre.name} for genre in genres]
