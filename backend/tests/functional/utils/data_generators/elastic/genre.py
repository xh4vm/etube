"""
Генерации фейковых данных, которые используются для тестов.

"""

from .base import BaseElasticDataGenerator
from ...fake_models.genre import FakeGenreFull
from ...fake_models.film import FakeFilmGenreRel


class GenreDataGenerator(BaseElasticDataGenerator):
    index = 'genres'
    fake_model = FakeGenreFull
    response_model = FakeFilmGenreRel
