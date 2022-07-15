"""
Преобразование данных для загрузки в ES.

На основе полученных от Postgres данных формируется массив,
пригодный для загрузки в ES. По последнему документу определяется
время изменения данных в ES.

"""

import json
from typing import Any, Iterator, Optional, Union

from models import Film, Genre, Person


class Transformer:

    def __init__(self):
        self.data_str = ''
        self.updated_at = None

    def transform_films(self, batch: list) -> tuple:
        for film in batch:
            film_data = Film(**dict(zip(film.keys(), film)))
            self.updated_at = film_data.updated_at.strftime('%Y-%m-%d %H:%M:%S.%f%z')
            self.data_str += json.dumps(
                {
                    'index': {
                        '_index': 'movies',
                        '_id': str(film_data.id),
                    },
                },
            ) + '\n'
            self.data_str += json.dumps(
                {
                    'id': str(film_data.id),
                    'imdb_rating': film_data.rating,
                    'genre': film_data.genres,
                    'title': film_data.title,
                    'description': film_data.description,
                    'director': self._get_short_persons(film_data.directors),
                    'actors_names': self._get_short_persons(film_data.actors),
                    'writers_names': self._get_short_persons(film_data.writers),
                    'actors': film_data.actors,
                    'writers': film_data.writers,
                },
            ) + '\n'

        return self.data_str, self.updated_at

    def _get_short_persons(self, persons: Optional[list[dict[str, Any]]]) -> Union[Iterator[str], tuple]:
        """Метод разворачивания словарей с персонами в массив имен"""
        return [person['name'] for person in persons] if persons is not None else []

    def transform_genres(self, batch: list) -> tuple:
        for genre in batch:
            genre_data = Genre(**dict(zip(genre.keys(), genre)))
            self.updated_at = genre_data.updated_at.strftime('%Y-%m-%d %H:%M:%S.%f%z')
            self.data_str += json.dumps(
                {
                    'index': {
                        '_index': 'genres',
                        '_id': str(genre_data.id),
                    },
                },
            ) + '\n'
            self.data_str += json.dumps(
                {
                    'id': str(genre_data.id),
                    'name': genre_data.name,
                    'description': genre_data.descr,
                },
            ) + '\n'

        return self.data_str, self.updated_at

    def transform_persons(self, batch: list) -> tuple:
        for person in batch:
            person_data = Person(**dict(zip(person.keys(), person)))
            self.updated_at = person_data.updated_at.strftime('%Y-%m-%d %H:%M:%S.%f%z')
            self.data_str += json.dumps(
                {
                    'index': {
                        '_index': 'persons',
                        '_id': str(person_data.id),
                    },
                },
            ) + '\n'
            self.data_str += json.dumps(
                {
                    'id': str(person_data.id),
                    'full_name': person_data.name,
                },
            ) + '\n'

        return self.data_str, self.updated_at
