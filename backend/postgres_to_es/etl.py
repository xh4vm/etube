"""
Базовый файл сервиса.

Пошагово запускаются отдельные этапы трансфера данных:
1. Запрашивается время последнего обновленного документа в ES.
2. Загружаются новые данные из Postgres.
3. Данные адаптируются для загрузки в ES.
4. Данные загружаются в ES по частям.
5. После выполнения загрузки в ES каждой части данных происходит
обновление параметра es_modified (время последнего обновленного документа).

"""


from http import HTTPStatus

from celery import Celery

from config import CELERY_CONFIG, POSTGRES_DSN, REDIS_CONFIG
from extractor import PostgreSQLExtractor
from loader import Loader
from logger import manager_logger as logger
from state import RedisState
from transformer import Transformer

celery = Celery(CELERY_CONFIG.name, backend=CELERY_CONFIG.backend, broker=CELERY_CONFIG.broker)

@celery.task
def transfer(extractor_method: str, transformer_method: str, index: str) -> None:
    logger.info('Запуск трансфера данных.')
    # Время последнего обновления данных в ES.
    etl_state = RedisState(settings=REDIS_CONFIG)

    # Обновленные данные в Postgres.
    pg_extractor = PostgreSQLExtractor(dsn=POSTGRES_DSN, state=etl_state)
    raw_data = getattr(pg_extractor, extractor_method)()

    # Преобразование данных для загрузки в ES.
    transformer = Transformer()
    loader = Loader(index)

    for batch in raw_data:
        data_to_load, updated_at = getattr(transformer, transformer_method)(batch)

        # Загрузка данных в ES.
        tail = ''.join(['/', index, '/_bulk'])
        response = loader.connector(tail=tail, data=data_to_load)

        # Изменение значения времени последнего обновления данных в ES.
        if response and response.status_code == HTTPStatus.OK:
            etl_state.set(f'bottom_limit_{index}', updated_at)
    logger.info('Трансфер данных завершен.')


@celery.on_after_configure.connect
def setup_etl_periodic_task(sender, **kwargs):
    sender.add_periodic_task(30.0, transfer.s('find_modified_films', 'transform_films', 'movies'), name='Update ETL every 30 seconds.')


if __name__ == '__main__':
    setup_etl_periodic_task(celery)
    transfer('find_modified_films', 'transform_films', 'movies')
