from ...fake_models.film import FakeFilmPersonRel
from ...fake_models.person import FakePersonFull
from .base import BaseElasticDataGenerator


class PersonDataGenerator(BaseElasticDataGenerator):
    index = 'persons'
    fake_model = FakePersonFull
    response_model = FakeFilmPersonRel
