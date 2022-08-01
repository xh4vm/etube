"""
Генерации фейковых данных, которые используются для тестов.

"""

import json
from abc import abstractmethod
from typing import Any
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from pydantic import ValidationError
from pydantic.main import ModelMetaclass

from ..base import BaseDataGenerator


class BaseElasticDataGenerator(BaseDataGenerator):
    conn = None

    @property
    @abstractmethod
    def index(self) -> str:
        '''Наименование индекса'''

    def __init__(self, conn: AsyncElasticsearch) -> None:
        self.conn = conn

    async def load(self):
        fake_data: list[ModelMetaclass] = []

        #TODO: bad locally
        with open(f'/opt/tests/functional/testdata/{self.index}.json', 'r') as fd:
            fake_data = json.load(fd)

        fake_models = (self.fake_model.parse_obj(elem) for elem in fake_data)
        self.data = self.data_wrapper(fake_docs=fake_models)

        print('AAAAAA', self.data)
        await async_bulk(self.conn, self.data)

    async def clean(self):
        docs_to_delete = [{'_op_type': 'delete', '_index': self.index, '_id': doc['_id']} for doc in self.data]
        await async_bulk(self.conn, docs_to_delete)

    def data_wrapper(self, fake_docs: list[ModelMetaclass]) -> list[str, Any]:
        return [
            {
                '_index': self.index,
                '_id': doc.id,
                '_source': doc.dict()
            }
            for doc in fake_docs
        ]
