"""Загрузчик данных из SQLite и загрузчик данных в Postgres."""

import sqlite3
from typing import Generator

from psycopg2.extensions import connection as _connection
from psycopg2.extras import execute_values

from logger import logger

# Размер партии данных для выгрузки из sqlite и загруки в postgres.
BATCH_SIZE = 100


class SQLiteLoader:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self.conn.row_factory = sqlite3.Row
        self.curs = conn.cursor()

    def load_data(self, table: str) -> Generator[str, list, None]:
        query = f'SELECT * FROM {table};'
        try:
            self.curs.execute(query)
        except Exception as error:
            logger.error(f'Ошибка выгрузки данных из таблицы {table}: {error}')
        while results := self.curs.fetchmany(BATCH_SIZE):
            yield results


class PostgresSaver:
    def __init__(self, conn: _connection):
        self.conn = conn
        self.curs = conn.cursor()

    def save_data(self, query: str, data: list) -> None:
        try:
            execute_values(self.curs, query, data)
        except Exception as error:
            logger.error(f'Ошибка загрузки данных: {error}')
        else:
            self.conn.commit()
