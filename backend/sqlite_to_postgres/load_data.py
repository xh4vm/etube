import os
import pathlib
import sqlite3
from typing import Any

import psycopg2

from psycopg2.extras import DictCursor, register_uuid
from contextlib import contextmanager
from dotenv import load_dotenv
import logging

from sqlite_loader import SQLiteLoader
from postgres_saver import PostgresSaver


@contextmanager
def sqlite_conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    yield conn

    conn.close()


@contextmanager
def pg_conn_context(postgresql_dsl: dict[str, Any]):
    conn = psycopg2.connect(**postgresql_dsl, cursor_factory=DictCursor)

    yield conn

    conn.close()


def load_from_sqlite(connection: sqlite3.Connection, pg_cursor: DictCursor) -> None:
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_cursor)
    sqlite_loader = SQLiteLoader(connection)

    data = sqlite_loader.load_movies()
    postgres_saver.save_all_data(data)


def get_postgresql_dsl() -> dict[str, Any]:
    return {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': os.environ.get('DB_PORT', 5432),
    }


if __name__ == '__main__':
    logging.root.setLevel(logging.NOTSET)
    logging.basicConfig(level=logging.NOTSET)

    load_dotenv()

    postgresql_dsl = get_postgresql_dsl()
    sqlite_path = os.environ.get('SQLITE_PATH')
    schema_file = os.path.join(pathlib.Path(__file__).parent.absolute(), 'schema.sql')

    with sqlite_conn_context(sqlite_path) as sqlite_conn, pg_conn_context(
        postgresql_dsl
    ) as pg_conn, pg_conn.cursor() as pg_cursor:

        with open(schema_file, 'r') as schema_fd:
            pg_cursor.execute(schema_fd.read())

        register_uuid()
        load_from_sqlite(sqlite_conn, pg_cursor)
