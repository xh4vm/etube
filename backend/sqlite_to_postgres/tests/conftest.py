import os

import pytest
from dotenv import load_dotenv
from load_data import get_postgresql_dsl, pg_conn_context, sqlite_conn_context

load_dotenv()

postgresql_dsl = get_postgresql_dsl()
sqlite_path = os.environ.get('SQLITE_PATH')


@pytest.fixture()
def sqlite_cursor():

    with sqlite_conn_context(sqlite_path) as sqlite_conn:

        yield sqlite_conn.cursor()


@pytest.fixture()
def pg_cursor():

    with pg_conn_context(postgresql_dsl) as pg_conn, pg_conn.cursor() as pg_cursor:

        yield pg_cursor
