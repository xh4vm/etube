import json
from abc import abstractmethod
from typing import Any
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk
from pydantic.main import ModelMetaclass

from ..base import BaseDataGenerator
from functional.settings import CONFIG


class BaseElasticDataGenerator(BaseDataGenerator):
    '''Генерации фейковых данных, которые используются для тестов.'''
    
    conn = None
    data = []

    @property
    @abstractmethod
    def index(self) -> str:
        '''Наименование индекса'''

    def __init__(self, conn: AsyncElasticsearch) -> None:
        self.conn = conn

    async def load(self):
        fake_data: list[ModelMetaclass] = []
        elastic_data: list[ModelMetaclass] = []
        response_data: list[ModelMetaclass] = []

        with open(f'{CONFIG.BASE_DIR}/testdata/{self.index}.json', 'r') as fd:
            fake_data = json.load(fd)

        for elem in fake_data:
            model = self.fake_model.parse_obj(elem)
            elastic_data.append(model)
            response_data.append(self.response_model.parse_obj({**elem, **model.dict()}))
     
        self.data = self._data_wrapper(fake_docs=elastic_data)
        await async_bulk(self.conn, self.data)
        await self.conn.indices.refresh(index=self.index)

        return self._data_wrapper(response_data)

    async def clean(self):
        docs_to_delete = [{'_op_type': 'delete', '_index': self.index, '_id': doc['_id']} for doc in self.data]
        await async_bulk(self.conn, docs_to_delete)

    def _data_wrapper(self, fake_docs: list[ModelMetaclass]) -> list[dict[str, Any]]:
        return [
            {
                '_index': self.index,
                '_id': doc.id,
                '_source': doc.dict()
            }
            for doc in fake_docs
        ]
