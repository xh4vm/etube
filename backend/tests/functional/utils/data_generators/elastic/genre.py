from ...fake_models.film import FakeFilmGenreRel
from ...fake_models.genre import FakeGenreFull
from .base import BaseElasticDataGenerator


class GenreDataGenerator(BaseElasticDataGenerator):
    index = 'genres'
    fake_model = FakeGenreFull
    response_model = FakeFilmGenreRel
