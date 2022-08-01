"""
Генерации фейковых данных, которые используются для тестов.

"""

from .base import BaseElasticDataGenerator
from ...fake_models import FakeGenre


class GenreDataGenerator(BaseElasticDataGenerator):
    index = 'genres'
    fake_model = FakeGenre
    data = []
