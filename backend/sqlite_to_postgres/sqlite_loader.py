import logging
import sqlite3
from typing import Any, Iterator

from handlers import (FilmWorkHandler, GenreFilmWorkHandler, GenreHandler,
                      PersonFilmWorkHandler, PersonHandler)
from schema import Schema


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class SQLiteLoader:
    def __init__(self, connection: sqlite3.Connection, chunk_size: int = 100) -> None:
        self.conn = connection
        self.curs = self.conn.cursor()
        self.chunk_size = chunk_size
        self.logger = logging.getLogger(__name__)

    def load_movies(self) -> Iterator[type]:
        query = (
            f'SELECT m.id as {Schema.film_work}_id, m.title as {Schema.film_work}_title, '
            f'm.description as {Schema.film_work}_description, m.creation_date as {Schema.film_work}_creation_date, '
            f'm.file_path as {Schema.film_work}_file_path, m.rating as {Schema.film_work}_rating, '
            f'm.type as {Schema.film_work}_type, m.created_at as {Schema.film_work}_created_at, '
            f'm.updated_at as {Schema.film_work}_updated_at, g.id as {Schema.genre}_id, '
            f'g.name as {Schema.genre}_name, g.description as {Schema.genre}_description, '
            f'g.created_at as {Schema.genre}_created_at, g.updated_at as {Schema.genre}_updated_at, '
            f'p.id as {Schema.person}_id, p.full_name as {Schema.person}_full_name, '
            f'p.created_at as {Schema.person}_created_at, p.updated_at as {Schema.person}_updated_at, '
            f'mg.id as {Schema.genre_film_work}_id, mg.film_work_id as {Schema.genre_film_work}_film_work_id, '
            f'mg.genre_id as {Schema.genre_film_work}_genre_id, mg.created_at as {Schema.genre_film_work}_created_at, '
            f'mp.id as {Schema.person_film_work}_id, mp.film_work_id as {Schema.person_film_work}_film_work_id, '
            f'mp.person_id as {Schema.person_film_work}_person_id, '
            f'mp.created_at as {Schema.person_film_work}_created_at, mp.role as {Schema.person_film_work}_role '
            f'FROM film_work m '
            f'LEFT JOIN genre_film_work mg ON mg.film_work_id = m.id '
            f'LEFT JOIN genre g ON mg.genre_id = g.id '
            f'LEFT JOIN person_film_work mp ON mp.film_work_id = m.id '
            f'LEFT JOIN person p ON mp.person_id = p.id;'
        )
        data = {
            Schema.genre: None,
            Schema.person: None,
            Schema.film_work: None,
            Schema.genre_film_work: None,
            Schema.person_film_work: None,
        }
        raw_objects = None
        self.curs.execute(query)

        while raw_objects != []:
            raw_objects: list[dict[str, Any]] = self.curs.fetchmany(self.chunk_size)

            self.logger.debug(f'Fetching {len(raw_objects)} objects.')

            for raw_object in raw_objects:
                raw_object = dict_factory(self.curs, raw_object)

                data[Schema.genre] = GenreHandler(
                    id=raw_object[f'{Schema.genre}_id'],
                    name=raw_object[f'{Schema.genre}_name'],
                    description=raw_object[f'{Schema.genre}_description'],
                    created_at=raw_object[f'{Schema.genre}_created_at'],
                    updated_at=raw_object[f'{Schema.genre}_updated_at'],
                ).get_dataclass()

                data[Schema.person] = PersonHandler(
                    id=raw_object[f'{Schema.person}_id'],
                    full_name=raw_object[f'{Schema.person}_full_name'],
                    created_at=raw_object[f'{Schema.person}_created_at'],
                    updated_at=raw_object[f'{Schema.person}_updated_at'],
                ).get_dataclass()

                data[Schema.film_work] = FilmWorkHandler(
                    id=raw_object[f'{Schema.film_work}_id'],
                    title=raw_object[f'{Schema.film_work}_title'],
                    description=raw_object[f'{Schema.film_work}_description'],
                    creation_date=raw_object[f'{Schema.film_work}_creation_date'],
                    file_path=raw_object[f'{Schema.film_work}_file_path'],
                    rating=raw_object[f'{Schema.film_work}_rating'],
                    type=raw_object[f'{Schema.film_work}_type'],
                    created_at=raw_object[f'{Schema.film_work}_created_at'],
                    updated_at=raw_object[f'{Schema.film_work}_updated_at'],
                ).get_dataclass()

                data[Schema.genre_film_work] = GenreFilmWorkHandler(
                    id=raw_object[f'{Schema.genre_film_work}_id'],
                    film_work_id=raw_object[f'{Schema.genre_film_work}_film_work_id'],
                    genre_id=raw_object[f'{Schema.genre_film_work}_genre_id'],
                    created_at=raw_object[f'{Schema.genre_film_work}_created_at'],
                ).get_dataclass()

                data[Schema.person_film_work] = PersonFilmWorkHandler(
                    id=raw_object[f'{Schema.person_film_work}_id'],
                    film_work_id=raw_object[f'{Schema.person_film_work}_film_work_id'],
                    person_id=raw_object[f'{Schema.person_film_work}_person_id'],
                    role=raw_object[f'{Schema.person_film_work}_role'],
                    created_at=raw_object[f'{Schema.person_film_work}_created_at'],
                ).get_dataclass()

                yield data
