"""
Генерации фейковых данных, которые используются для тестов.

"""

from .base import BaseElasticDataGenerator
from ...fake_models.person import FakePersonFull
from ...fake_models.film import FakeFilmPersonRel


class PersonDataGenerator(BaseElasticDataGenerator):
    index = 'persons'
    fake_model = FakePersonFull
    response_model = FakeFilmPersonRel
