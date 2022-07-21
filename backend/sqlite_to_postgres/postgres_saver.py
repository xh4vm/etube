import logging
from dataclasses import asdict, fields, is_dataclass
from typing import Any, Iterator, Optional

from psycopg2.extras import DictCursor, execute_values
from schema import (SCHEMA_NAME, FilmWork, Genre, GenreFilmWork, Person,
                    PersonFilmWork, Schema)


class PostgresSaver:
    def __init__(self, pg_cursor: DictCursor, chunk_size: int = 100):
        self.curs = pg_cursor
        self.metadata = {
            Schema.genre: Genre,
            Schema.person: Person,
            Schema.film_work: FilmWork,
            Schema.genre_film_work: GenreFilmWork,
            Schema.person_film_work: PersonFilmWork,
        }
        self.loaded_data = {schema_name: [] for schema_name in self.metadata.keys()}
        self.chunk_size = chunk_size
        self.logger = logging.getLogger(__name__)

    def _multiple_insert(self, insert_query: str, data: list[tuple[Any]]) -> None:
        execute_values(self.curs, insert_query, data)

    def _get_values_statement(self, into_statement: list[str], data: type) -> tuple[Any]:
        data_as_dict: dict[str, Any] = asdict(data)
        return tuple(data_as_dict[key] for key in into_statement)

    def _save_data(self, schema_name: str) -> None:
        schema: type = self.metadata.get(schema_name)
        data: Iterator[type] = self.loaded_data[schema_name]

        if not is_dataclass(schema):
            message = f'Error with saving dataclass: {schema_name}. Message: is not dataclass type.'
            self.logger.error(message)
            raise TypeError(message)

        into_statement: list[str] = [field.name for field in fields(schema)]
        insert_query: str = (
            f'INSERT INTO {SCHEMA_NAME}.{schema_name}'
            f'({", ".join(into_statement)}) '
            f'VALUES %s ON CONFLICT (id) DO NOTHING'
        )

        self._multiple_insert(
            insert_query, (self._get_values_statement(into_statement=into_statement, data=elem) for elem in data),
        )

        self.logger.debug(f'Success multiple insert {schema_name} ({len(data)} objects)')

    def _stack_or_flush(self, schema_name: str, data: Optional[type], is_last: bool):
        if data is not None:
            self.loaded_data[schema_name].append(data)

        if len(self.loaded_data[schema_name]) == self.chunk_size or is_last:
            self._save_data(schema_name=schema_name)
            self.loaded_data.update({schema_name: []})
            self.logger.debug(f'Chunk from {schema_name} schema has been flushed!')

    def _stack_or_flush_all_data(self, obj: dict[str, type], is_last: bool = False) -> None:
        try:

            for schema_name in self.metadata.keys():
                self._stack_or_flush(schema_name=schema_name, data=obj[schema_name], is_last=is_last)

            self.curs.execute('COMMIT;')

        except Exception as err:
            self.curs.execute('ROLLBACK;')

            self.logger.error(f'Error stack or flush data! Message: {err}')
            raise err

    def save_all_data(self, data: Iterator[dict[str, type]]) -> None:
        last_obj = {
            Schema.genre: None,
            Schema.person: None,
            Schema.film_work: None,
            Schema.genre_film_work: None,
            Schema.person_film_work: None,
        }

        self.logger.info('Start saving all data to PostgreSQL database instance.')

        for obj in data:
            self._stack_or_flush_all_data(obj)

        self._stack_or_flush_all_data(obj=last_obj, is_last=True)

        self.logger.info('Success finish saving all data to PostgreSQL database instance.')
