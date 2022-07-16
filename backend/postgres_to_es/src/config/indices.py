# Классы, определяющие параметры переноса данных
# из Postgres в ES, включая названия индексов.

from etl.extractor import (FilmsPostgresExtractor, GenresPostgresExtracor,
                           PersonsPostgresExtractor)
from models.models import Film, Genre, Person


class FilmIndex:
    extractor = FilmsPostgresExtractor
    model = Film
    index = 'movies'

class GenreIndex:
    extractor = GenresPostgresExtracor
    model = Genre
    index = 'genres'

class PersonIndex:
    extractor = PersonsPostgresExtractor
    model = Person
    index = 'persons'
