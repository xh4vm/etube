from sqlite3 import Cursor
from psycopg2.extras import DictCursor
from schema import Schema, SCHEMA_NAME


class TestCountRecords:
    def test_count_genre_records(self, sqlite_cursor: Cursor, pg_cursor: DictCursor):

        sqlite_query = f'SELECT COUNT(*) FROM {Schema.genre};'
        sqlite_cursor.execute(sqlite_query)
        count_in_sqlite = sqlite_cursor.fetchone()

        pg_query = f'SELECT COUNT(*) FROM {SCHEMA_NAME}.{Schema.genre};'
        pg_cursor.execute(pg_query)
        count_in_pg = pg_cursor.fetchone()

        assert count_in_sqlite[0] == count_in_pg[0]

    def test_count_person_records(self, sqlite_cursor: Cursor, pg_cursor: DictCursor):

        sqlite_query = f'SELECT COUNT(*) FROM {Schema.person};'
        sqlite_cursor.execute(sqlite_query)
        count_in_sqlite = sqlite_cursor.fetchone()

        pg_query = f'SELECT COUNT(*) FROM {SCHEMA_NAME}.{Schema.person};'
        pg_cursor.execute(pg_query)
        count_in_pg = pg_cursor.fetchone()

        assert count_in_sqlite[0] == count_in_pg[0]

    def test_count_film_works_records(self, sqlite_cursor: Cursor, pg_cursor: DictCursor):

        sqlite_query = f'SELECT COUNT(*) FROM {Schema.film_work};'
        sqlite_cursor.execute(sqlite_query)
        count_in_sqlite = sqlite_cursor.fetchone()

        pg_query = f'SELECT COUNT(*) FROM {SCHEMA_NAME}.{Schema.film_work};'
        pg_cursor.execute(pg_query)
        count_in_pg = pg_cursor.fetchone()

        assert count_in_sqlite[0] == count_in_pg[0]

    def test_count_genre_film_works_records(self, sqlite_cursor: Cursor, pg_cursor: DictCursor):

        sqlite_query = f'SELECT COUNT(*) FROM {Schema.genre_film_work};'
        sqlite_cursor.execute(sqlite_query)
        count_in_sqlite = sqlite_cursor.fetchone()

        pg_query = f'SELECT COUNT(*) FROM {SCHEMA_NAME}.{Schema.genre_film_work};'
        pg_cursor.execute(pg_query)
        count_in_pg = pg_cursor.fetchone()

        assert count_in_sqlite[0] == count_in_pg[0]

    def test_count_person_film_works_records(self, sqlite_cursor: Cursor, pg_cursor: DictCursor):

        sqlite_query = f'SELECT COUNT(*) FROM {Schema.person_film_work};'
        sqlite_cursor.execute(sqlite_query)
        count_in_sqlite = sqlite_cursor.fetchone()

        pg_query = f'SELECT COUNT(*) FROM {SCHEMA_NAME}.{Schema.person_film_work};'
        pg_cursor.execute(pg_query)
        count_in_pg = pg_cursor.fetchone()

        assert count_in_sqlite[0] == count_in_pg[0]
