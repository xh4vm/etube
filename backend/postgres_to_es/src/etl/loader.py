"""
Загрузчик данных в индекс movies ES.

При загрузке данных в индекс функция connector отдает код ответа
(или None, если ES не доступен). Только если код ответа 200
в постоянное хранилище запишется время последнего обновления.

"""

from typing import Any

import backoff
import requests

from config.config import BACKOFF_CONFIG, ELASTIC_CONFIG
from logger.logger import loader_logger as logger


class Loader:

    def __init__(self, index: str):
        self.params = ELASTIC_CONFIG.dict()
        self.protocol = self.params.get('protocol')
        self.host = self.params.get('host')
        self.port = self.params.get('port')
        self.index_name = index

    @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    def connector(
        self,
        index: str,
        data: Any = None,
    ) -> Any:
        url = ''.join([self.protocol, '://', self.host, ':', str(self.port), '/', index, '/_bulk'])
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, data=data, headers=headers)
        return response
