from typing import Any, Optional

import backoff
from config.base import BACKOFF_CONFIG, ElasticsearchSettings
from config.logger import logger
from elasticsearch import Elasticsearch


def es_conn_is_alive(es_conn: Elasticsearch) -> bool:
    """Функция для проверки работоспособности Elasticsearch"""
    try:
        return es_conn.ping()
    except Exception:
        return False


class ElasticIniter:
    def __init__(self, settings: ElasticsearchSettings, conn: Optional[Elasticsearch] = None) -> None:
        self._conn: Elasticsearch = conn
        self._settings: ElasticsearchSettings = settings

    @property
    def conn(self) -> Elasticsearch:
        if self._conn is None or not es_conn_is_alive(self._conn):
            self._conn = self._reconnection()

        return self._conn

    @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    def _reconnection(self) -> Elasticsearch:
        logger.info('Reconnection elasticsearch...')

        if self._conn is not None:
            logger.info('Closing already exists es connector...')
            self._conn.close()

        return Elasticsearch(
            [
                (
                    f'{self._settings.protocol}://{self._settings.user}:{self._settings.password}'
                    f'@{self._settings.host}:{self._settings.port}'
                )
            ]
        )

    @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    def create(self, index_name: str, mapping: dict[str, Any]):
        if self.conn.indices.exists(index_name):
            logger.info(f'[+] Index "{index_name}" already exists!')
        else:
            logger.info(f'[?] Creating index "{index_name}" with map...')
            self.conn.indices.create(index=index_name, body=mapping)
            logger.info(f'[+] Successfull creating index "{index_name}"!')
