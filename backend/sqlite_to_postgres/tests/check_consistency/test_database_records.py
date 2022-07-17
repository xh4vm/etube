from sqlite3 import Cursor
from psycopg2.extras import DictCursor

from sqlite_loader import dict_factory
from schema import Schema, SCHEMA_NAME, Genre, Person, FilmWork, GenreFilmWork, PersonFilmWork
from handlers import GenreHandler, PersonHandler, FilmWorkHandler, GenreFilmWorkHandler, PersonFilmWorkHandler


class TestDatabaseRecords:
    limit = 10

    def test_top_limit_genre_records_asc_id(self, sqlite_cursor: Cursor, pg_cursor: DictCursor):

        sqlite_query = f'SELECT * FROM {Schema.genre} ORDER BY id;'
        sqlite_cursor.execute(sqlite_query)
        raw_in_sqlite: list = sqlite_cursor.fetchmany(self.limit)
        sqlite_result: list[Genre] = [
            GenreHandler(**dict_factory(sqlite_cursor, raw_genre)).get_dataclass() for raw_genre in raw_in_sqlite
        ]

        pg_query = f'SELECT * FROM {SCHEMA_NAME}.{Schema.genre} ORDER BY id;'
        pg_cursor.execute(pg_query)
        raw_in_pg: list = pg_cursor.fetchmany(self.limit)
        pg_result: list[Genre] = [GenreHandler(**raw_genre).get_dataclass() for raw_genre in raw_in_pg]

        assert sqlite_result == pg_result

    def test_top_limit_genre_records_desc_id(self, sqlite_cursor: Cursor, pg_cursor: DictCursor):

        sqlite_query = f'SELECT * FROM {Schema.genre} ORDER BY id DESC;'
        sqlite_cursor.execute(sqlite_query)
        raw_in_sqlite: list = sqlite_cursor.fetchmany(self.limit)
        sqlite_result: list[Genre] = [
            GenreHandler(**dict_factory(sqlite_cursor, raw_genre)).get_dataclass() for raw_genre in raw_in_sqlite
        ]

        pg_query = f'SELECT * FROM {SCHEMA_NAME}.{Schema.genre} ORDER BY id DESC;'
        pg_cursor.execute(pg_query)
        raw_in_pg: list = pg_cursor.fetchmany(self.limit)
        pg_result: list[Genre] = [GenreHandler(**raw_genre).get_dataclass() for raw_genre in raw_in_pg]

        assert sqlite_result == pg_result

    def test_top_limit_person_records_asc_id(self, sqlite_cursor: Cursor, pg_cursor: DictCursor):

        sqlite_query = f'SELECT * FROM {Schema.person} ORDER BY id;'
        sqlite_cursor.execute(sqlite_query)
        raw_in_sqlite: list = sqlite_cursor.fetchmany(self.limit)
        sqlite_result: list[Person] = [
            PersonHandler(**dict_factory(sqlite_cursor, raw_person)).get_dataclass() for raw_person in raw_in_sqlite
        ]

        pg_query = f'SELECT * FROM {SCHEMA_NAME}.{Schema.person} ORDER BY id;'
        pg_cursor.execute(pg_query)
        raw_in_pg: list = pg_cursor.fetchmany(self.limit)
        pg_result: list[Person] = [PersonHandler(**raw_person).get_dataclass() for raw_person in raw_in_pg]

        assert sqlite_result == pg_result

    def test_top_limit_person_records_desc_id(self, sqlite_cursor: Cursor, pg_cursor: DictCursor):

        sqlite_query = f'SELECT * FROM {Schema.person} ORDER BY id DESC;'
        sqlite_cursor.execute(sqlite_query)
        raw_in_sqlite: list = sqlite_cursor.fetchmany(self.limit)
        sqlite_result: list[Person] = [
            PersonHandler(**dict_factory(sqlite_cursor, raw_person)).get_dataclass() for raw_person in raw_in_sqlite
        ]

        pg_query = f'SELECT * FROM {SCHEMA_NAME}.{Schema.person} ORDER BY id DESC;'
        pg_cursor.execute(pg_query)
        raw_in_pg: list = pg_cursor.fetchmany(self.limit)
        pg_result: list[Person] = [PersonHandler(**raw_person).get_dataclass() for raw_person in raw_in_pg]

        assert sqlite_result == pg_result

    def test_top_limit_film_work_records_asc_id(self, sqlite_cursor: Cursor, pg_cursor: DictCursor):

        sqlite_query = f'SELECT * FROM {Schema.film_work} ORDER BY id;'
        sqlite_cursor.execute(sqlite_query)
        raw_in_sqlite: list = sqlite_cursor.fetchmany(self.limit)
        sqlite_result: list[FilmWork] = [
            FilmWorkHandler(**dict_factory(sqlite_cursor, raw_film_work)).get_dataclass()
            for raw_film_work in raw_in_sqlite
        ]

        pg_query = f'SELECT * FROM {SCHEMA_NAME}.{Schema.film_work} ORDER BY id;'
        pg_cursor.execute(pg_query)
        raw_in_pg: list = pg_cursor.fetchmany(self.limit)
        pg_result: list[FilmWork] = [FilmWorkHandler(**raw_film_work).get_dataclass() for raw_film_work in raw_in_pg]

        assert sqlite_result == pg_result

    def test_top_limit_film_work_records_desc_id(self, sqlite_cursor: Cursor, pg_cursor: DictCursor):

        sqlite_query = f'SELECT * FROM {Schema.film_work} ORDER BY id DESC;'
        sqlite_cursor.execute(sqlite_query)
        raw_in_sqlite: list = sqlite_cursor.fetchmany(self.limit)
        sqlite_result: list[FilmWork] = [
            FilmWorkHandler(**dict_factory(sqlite_cursor, raw_film_work)).get_dataclass()
            for raw_film_work in raw_in_sqlite
        ]

        pg_query = f'SELECT * FROM {SCHEMA_NAME}.{Schema.film_work} ORDER BY id DESC;'
        pg_cursor.execute(pg_query)
        raw_in_pg: list = pg_cursor.fetchmany(self.limit)
        pg_result: list[FilmWork] = [FilmWorkHandler(**raw_film_work).get_dataclass() for raw_film_work in raw_in_pg]

        assert sqlite_result == pg_result

    def test_top_limit_genre_film_work_records_asc_id(self, sqlite_cursor: Cursor, pg_cursor: DictCursor):

        sqlite_query = f'SELECT * FROM {Schema.genre_film_work} ORDER BY id;'
        sqlite_cursor.execute(sqlite_query)
        raw_in_sqlite: list = sqlite_cursor.fetchmany(self.limit)
        sqlite_result: list[GenreFilmWork] = [
            GenreFilmWorkHandler(**dict_factory(sqlite_cursor, raw_genre_film_work)).get_dataclass()
            for raw_genre_film_work in raw_in_sqlite
        ]

        pg_query = f'SELECT * FROM {SCHEMA_NAME}.{Schema.genre_film_work} ORDER BY id;'
        pg_cursor.execute(pg_query)
        raw_in_pg: list = pg_cursor.fetchmany(self.limit)
        pg_result: list[GenreFilmWork] = [
            GenreFilmWorkHandler(**raw_genre_film_work).get_dataclass() for raw_genre_film_work in raw_in_pg
        ]

        assert sqlite_result == pg_result

    def test_top_limit_genre_film_work_records_desc_id(self, sqlite_cursor: Cursor, pg_cursor: DictCursor):

        sqlite_query = f'SELECT * FROM {Schema.genre_film_work} ORDER BY id DESC;'
        sqlite_cursor.execute(sqlite_query)
        raw_in_sqlite: list = sqlite_cursor.fetchmany(self.limit)
        sqlite_result: list[GenreFilmWork] = [
            GenreFilmWorkHandler(**dict_factory(sqlite_cursor, raw_genre_film_work)).get_dataclass()
            for raw_genre_film_work in raw_in_sqlite
        ]

        pg_query = f'SELECT * FROM {SCHEMA_NAME}.{Schema.genre_film_work} ORDER BY id DESC;'
        pg_cursor.execute(pg_query)
        raw_in_pg: list = pg_cursor.fetchmany(self.limit)
        pg_result: list[GenreFilmWork] = [
            GenreFilmWorkHandler(**raw_genre_film_work).get_dataclass() for raw_genre_film_work in raw_in_pg
        ]

        assert sqlite_result == pg_result

    def test_top_limit_person_film_work_records_asc_id(self, sqlite_cursor: Cursor, pg_cursor: DictCursor):

        sqlite_query = f'SELECT * FROM {Schema.person_film_work} ORDER BY id;'
        sqlite_cursor.execute(sqlite_query)
        raw_in_sqlite: list = sqlite_cursor.fetchmany(self.limit)
        sqlite_result: list[PersonFilmWork] = [
            PersonFilmWorkHandler(**dict_factory(sqlite_cursor, raw_genre_film_work)).get_dataclass()
            for raw_genre_film_work in raw_in_sqlite
        ]

        pg_query = f'SELECT * FROM {SCHEMA_NAME}.{Schema.person_film_work} ORDER BY id;'
        pg_cursor.execute(pg_query)
        raw_in_pg: list = pg_cursor.fetchmany(self.limit)
        pg_result: list[PersonFilmWork] = [
            PersonFilmWorkHandler(**raw_person_film_work).get_dataclass() for raw_person_film_work in raw_in_pg
        ]

        assert sqlite_result == pg_result

    def test_top_limit_person_film_work_records_desc_id(self, sqlite_cursor: Cursor, pg_cursor: DictCursor):

        sqlite_query = f'SELECT * FROM {Schema.person_film_work} ORDER BY id DESC;'
        sqlite_cursor.execute(sqlite_query)
        raw_in_sqlite: list = sqlite_cursor.fetchmany(self.limit)
        sqlite_result: list[PersonFilmWork] = [
            PersonFilmWorkHandler(**dict_factory(sqlite_cursor, raw_person_film_work)).get_dataclass()
            for raw_person_film_work in raw_in_sqlite
        ]

        pg_query = f'SELECT * FROM {SCHEMA_NAME}.{Schema.person_film_work} ORDER BY id DESC;'
        pg_cursor.execute(pg_query)
        raw_in_pg: list = pg_cursor.fetchmany(self.limit)
        pg_result: list[PersonFilmWork] = [
            PersonFilmWorkHandler(**raw_person_film_work).get_dataclass() for raw_person_film_work in raw_in_pg
        ]

        assert sqlite_result == pg_result
