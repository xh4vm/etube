"""
Входной файл.

Инициирует выгрузку данных из sqlite и загрузку в postgres (loaders.py)
с использованием моделей таблиц БД (models.py).
"""

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path

import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from loaders import PostgresSaver, SQLiteLoader
from models import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork

path = Path(__file__).resolve().parent.parent
load_dotenv(''.join([str(path), '/config/.env']))

dsl = {
    'dbname': os.environ.get('DB_NAME'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'port': int(os.environ.get('DB_PORT')),
}


@contextmanager
def sql_conn_context():
    conn = sqlite3.connect('./sqlite_to_postgres/db.sqlite')
    # conn = sqlite3.connect('./db.sqlite')
    yield conn
    conn.close()


@contextmanager
def pg_conn_context():
    conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    yield conn
    conn.close()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection) -> None:
    """
    Менеджер трансфера данных.

    1. Для каждой таблицы получаем данные из sqlite по частям (batch).
    2. Прогоняем полученные данные через датаклассы (d_class).
    3. Отправляем подготовленные для загрузки в БД данные в PostgresSaver.
    """
    sqlite_loader = SQLiteLoader(connection)
    postgres_saver = PostgresSaver(pg_conn)

    tables = {
        FilmWork: 'film_work',
        Person: 'person',
        Genre: 'genre',
        PersonFilmWork: 'person_film_work',
        GenreFilmWork: 'genre_film_work',
    }

    for d_class, db_table in tables.items():
        table_fields = d_class.get_slots()
        # Получаем порцию данных из sqlite.
        sqlite_data = sqlite_loader.load_data(db_table)
        for batch in sqlite_data:
            # Прогоняем данные через датаклассы.
            data_to_load = [d_class.get_values(item) for item in batch]
            query = f'INSERT INTO content.{db_table} ' \
                    f'({table_fields}) ' \
                    f'VALUES %s ON CONFLICT (id) DO NOTHING;'
            # Отправляем на загрузку в postgres.
            postgres_saver.save_data(query, data_to_load)

if __name__ == '__main__':
    with sql_conn_context() as sqlite_conn, pg_conn_context() as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
