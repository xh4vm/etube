"""
Преобразование данных для загрузки в ES.

На основе полученных от Postgres данных формируется массив,
пригодный для загрузки в ES. По последнему документу определяется
время изменения данных в ES.

"""

import json
import uuid

import pydantic

from ..logger.logger import transform_logger as logger


class Transformer:

    def __init__(self):
        self.data_str = ''
        self.updated_at = None

    def index_settings(self, index: str, id: uuid.UUID) -> str:
        # Общие настройки документа в индексе.
        return json.dumps(
                {
                    'index': {
                        '_index': index,
                        '_id': str(id),
                    },
                },
            ) + '\n'

    def transform_data(self, batch: list, index: str, model: pydantic.main.ModelMetaclass) -> tuple:
        # Валидация данных и трансформация для последующей загрузки в ES.
        for doc in batch:

            doc_data = model(**dict(zip(doc.keys(), doc)))
            self.updated_at = doc_data.updated_at.strftime('%Y-%m-%d %H:%M:%S.%f%z')
            self.data_str += self.index_settings(index, doc_data.id)
            self.data_str += json.dumps(doc_data.index_data()) + '\n'

        return self.data_str, self.updated_at
