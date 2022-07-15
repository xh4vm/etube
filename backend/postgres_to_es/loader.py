"""
Загрузчик данных в индекс movies ES.

При создании объекта Loader происходит проверка существования индекса.
Если индекс не сушествует, он создается.

В случае отсутствия соединения с ES рекурсивно вызывается функция connector
с увеличивающимся интервалом времени.

При загрузке данных в индекс функция connector отдает код ответа
(или None, если ES не доступен). Только если код ответа 200
в постоянное хранилище запишется время последнего обновления.

"""

import json
from http import HTTPStatus
from typing import Any

import backoff
import requests

from config import BACKOFF_CONFIG, ELASTIC_CONFIG
from elasticsearch.indices import genres, movies, persons
from logger import loader_logger as logger


class Loader:

    def __init__(self, index: str):
        indices = {
            'movies': movies.film_index,
            'genres': genres.genre_index,
            'persons': persons.person_index,
        }
        self.params = ELASTIC_CONFIG.dict()
        self.host = self.params.get('host')
        self.port = self.params.get('port')
        self.index_name = index
        self.index_schema = indices[self.index_name]
        # Проверка существования индекса при первом подключении.
        tail = ''.join(['/_cat/indices/', self.index_name])
        self.connector(tail=tail, req='get')

    @backoff.on_exception(**BACKOFF_CONFIG, logger=logger)
    def connector(
        self,
        tail: str,
        req: str = 'post',
        data: Any = None,
    ) -> Any:
        # req: тип запроса (get, put, post).
        # tail: хвост адреса для запроса.
        request_method = getattr(requests, req)
        url = ''.join([self.host, ':', str(self.port), tail])
        headers = {'Content-Type': 'application/json'}

        response = request_method(url, data=data, headers=headers)

        if req == 'get' and response.status_code == HTTPStatus.NOT_FOUND:
            # Создание индекса.
            tail = ''.join(['/', self.index_name])
            self.connector(tail=tail, req='put', data=json.dumps(self.index_schema))
            logger.info('Индекс ES создан.')
        return response
