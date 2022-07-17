from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Iterator, Optional

import backoff
import psycopg2
from psycopg2.extensions import connection
from psycopg2.extras import DictCursor

from ..config.config import BACKOFF_CONFIG, PostgreSQLSettings
from ..logger.logger import extractor_logger as logger
from ..models.schema import SCHEMA, PersonFilmWorkRoleEnum, Schema
from ..state.state import BaseState


class PostgreSQLExtractor(ABC):
    """Базовый класс для извлечения сырых данных из постгрес."""
    def __init__(
        self,
        index: str,
        dsn: PostgreSQLSettings,
        state: BaseState,
        pg_conn: Optional[connection] = None,
        chunk_size: int = 100,
    ):
        self.index = index
        self._pg_conn = pg_conn
        self._dsn = dsn
        self._state = state
        self.chunk_size = chunk_size
        self.cursor = self.pg_conn.cursor()
        self.bottom_limit = self._state.get(f'bottom_limit_{self.index}', default_value=str(datetime.min))
        logger.debug(f'{self.index} state set in self.bottom_limit')

    @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    def _reconnection(self) -> connection:
        """Метод подключения/переподключения к бд"""
        if self._pg_conn is not None:
            self._pg_conn.close()

        return psycopg2.connect(**self._dsn.dict(), cursor_factory=DictCursor)

    @property
    def pg_conn(self) -> connection:
        if self._pg_conn is None or self._pg_conn.closed:
            self._pg_conn = self._reconnection()

        return self._pg_conn

    @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    def executor(self, query) -> Iterator[tuple[Any]]:
        self.cursor.execute(query)
        while results := self.cursor.fetchmany(self.chunk_size):
            yield results
        self.cursor.close()

    @abstractmethod
    def find_modified_docs(self):
        pass


class FilmsPostgresExtractor(PostgreSQLExtractor):
    def find_modified_docs(self) -> Iterator[tuple[Any]]:
        """Метод получения сырых данных из бд.
        В результате возвращаю генератор, которых позволяет брать
        данные из бд сразу пачкой по chunk_size штук"""
        query = (
            f'SELECT fw.id, fw.title, fw.description, fw.rating AS imdb_rating, fw.creation_date, fw.type, '
            f'GREATEST(fw.updated_at, MAX(p.updated_at), MAX(g.updated_at)) as updated_at, '
            f"COALESCE(ARRAY_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) "
            f"FILTER (WHERE pfw.role = '{PersonFilmWorkRoleEnum.DIRECTOR}')," + " '{}') AS director, "
            f"COALESCE(ARRAY_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) "
            f"FILTER (WHERE pfw.role = '{PersonFilmWorkRoleEnum.ACTOR}')," + " '{}') AS actors, "
            f"COALESCE(ARRAY_AGG(DISTINCT jsonb_build_object('id', p.id, 'name', p.full_name)) "
            f"FILTER (WHERE pfw.role = '{PersonFilmWorkRoleEnum.WRITER}')," + " '{}') AS writers, "
            f'ARRAY_AGG(DISTINCT g.name) as genre FROM {SCHEMA}.{Schema.film_work} fw '
            f'LEFT JOIN {SCHEMA}.{Schema.person_film_work} AS pfw ON pfw.film_work_id = fw.id '
            f'LEFT JOIN {SCHEMA}.{Schema.person} AS p ON p.id = pfw.person_id '
            f'LEFT JOIN {SCHEMA}.{Schema.genre_film_work} AS gfw ON gfw.film_work_id = fw.id '
            f'LEFT JOIN {SCHEMA}.{Schema.genre} AS g ON g.id = gfw.genre_id '
            f"WHERE GREATEST(fw.updated_at, p.updated_at, g.updated_at) > '{self.bottom_limit}' "
            f'GROUP BY fw.id '
            f'ORDER BY GREATEST(fw.updated_at, MAX(p.updated_at), MAX(g.updated_at));'
        )
        return self.executor(query)


class GenresPostgresExtracor(PostgreSQLExtractor):
    def find_modified_docs(self) -> Iterator[tuple[Any]]:
        # Запрос на получение измененных жанров.
        query = (
            f"SELECT g.id, g.name, g.description, g.updated_at "
            f"FROM {SCHEMA}.genre g "
            f"WHERE g.updated_at > '{self.bottom_limit}'"
            f'ORDER BY g.updated_at;'
        )
        return self.executor(query)


class PersonsPostgresExtractor(PostgreSQLExtractor):
    def find_modified_docs(self) -> Iterator[tuple[Any]]:
        # Запрос на получение измененных персон.
        query = (
            f"SELECT p.id, p.full_name AS name, p.updated_at "
            f"FROM {SCHEMA}.person p "
            f"WHERE p.updated_at > '{self.bottom_limit}'"
            f'ORDER BY p.updated_at;'
        )
        return self.executor(query)
