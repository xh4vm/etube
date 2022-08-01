"""
Генерации фейковых данных, которые используются для тестов.

"""



from .base import BaseElasticDataGenerator
from ...fake_models import FakeFilm


class FilmDataGenerator(BaseElasticDataGenerator):
    index = 'movies'
    fake_model = FakeFilm
    data = []
