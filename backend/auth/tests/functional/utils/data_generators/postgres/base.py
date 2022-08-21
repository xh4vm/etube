import json
from abc import abstractmethod
from datetime import datetime
from typing import Any

from functional.settings import CONFIG
from psycopg2.extras import DictCursor, execute_values
from pydantic.main import ModelMetaclass

from ..base import BaseDataGenerator


class BasePostgresDataGenerator(BaseDataGenerator):
    """Генерации фейковых данных, которые используются для тестов."""

    conn = None
    data = []

    @property
    @abstractmethod
    def table(self) -> str:
        """Наименование таблицы"""

    def __init__(self, conn: DictCursor) -> None:
        self.conn = conn

    def _get_values_statement(self, into_statement: list[str], data: dict[str, Any]) -> tuple[Any]:
        return tuple(data[key] for key in into_statement)

    async def load(self):
        fake_data: list[ModelMetaclass] = []
        postgres_data: list[ModelMetaclass] = []

        with open(f'{CONFIG.BASE_DIR}/testdata/{self.table}.json', 'r') as fd:
            fake_data = json.load(fd)

        for elem in fake_data:
            model = self.fake_model.parse_obj(elem)
            postgres_data.append(model)

        self.data = self._data_wrapper(fake_docs=postgres_data)

        into_statement: list[str] = [field for field in model.dict().keys()]
        insert_query: str = (
            f'INSERT INTO {CONFIG.DB.SCHEMA_NAME}.{self.table}'
            f'({", ".join(into_statement)}) '
            f'VALUES %s ON CONFLICT (id) DO NOTHING'
        )

        execute_values(
            self.conn,
            insert_query,
            (self._get_values_statement(into_statement=into_statement, data=elem) for elem in self.data),
        )
        self.conn.execute('COMMIT;')

        return self.data

    async def clean(self):
        ids: list[list] = [[elem['id'] for elem in self.data]]
        delete_query: str = (f'DELETE FROM {CONFIG.DB.SCHEMA_NAME}.{self.table} ' f'WHERE id in %s')
        execute_values(self.conn, delete_query, ids)
        self.conn.execute('COMMIT;')

    def _data_wrapper(self, fake_docs: list[ModelMetaclass]) -> list[dict[str, Any]]:
        return [{**doc.dict(), 'created_at': datetime.utcnow(), 'updated_at': datetime.utcnow()} for doc in fake_docs]
