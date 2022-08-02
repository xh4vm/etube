"""
Генерации фейковых данных, которые используются для тестов.

"""



from .base import BaseElasticDataGenerator
from ...fake_models.film import FakeFilmFull


class FilmDataGenerator(BaseElasticDataGenerator):
    index = 'movies'
    fake_model = FakeFilmFull
    response_model = FakeFilmFull
