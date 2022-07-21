"""
Загрузчик данных в индекс movies ES.

При загрузке данных в индекс функция connector отдает код ответа
(или None, если ES не доступен). Только если код ответа 200
в постоянное хранилище запишется время последнего обновления.

"""

from http import HTTPStatus
from typing import Any

import backoff
import requests

from ..config.config import BACKOFF_CONFIG, ELASTIC_CONFIG
from ..logger.logger import loader_logger as logger


class Loader:
    def __init__(self, index: str):
        self.index_name = index

    @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    def connector(self, index: str, data: Any = None,) -> Any:

        url = f'{ELASTIC_CONFIG.protocol}://{ELASTIC_CONFIG.host}:{ELASTIC_CONFIG.port}/{index}/_bulk'
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=data, headers=headers)

        logger.info(f'Response load status code: {response.status_code}')

        if response.status_code != HTTPStatus.OK:
            logger.info(f'Response content: {response.content}')
            raise ValueError('Loader failed...')

        return response
