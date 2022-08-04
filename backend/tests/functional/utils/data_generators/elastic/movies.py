from ...fake_models.film import FakeFilmFull
from .base import BaseElasticDataGenerator


class FilmDataGenerator(BaseElasticDataGenerator):
    index = 'movies'
    fake_model = FakeFilmFull
    response_model = FakeFilmFull
