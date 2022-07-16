"""
Базовый файл сервиса.

Пошагово запускаются отдельные этапы трансфера данных:
1. Запрашивается время последнего обновленного документа в ES.
2. Загружаются новые данные из Postgres.
3. Данные адаптируются для загрузки в ES.
4. Данные загружаются в ES по частям.
5. После выполнения загрузки в ES каждой части данных происходит
обновление параметра etl_state (время последнего обновленного документа).

"""

from http import HTTPStatus

import pydantic
from celery import Celery

from config.config import CELERY_CONFIG, POSTGRES_DSN, REDIS_CONFIG
from config.indices import FilmIndex, GenreIndex, PersonIndex
from etl.loader import Loader
from etl.transformer import Transformer
from logger.logger import manager_logger as logger
from state.state import RedisState

celery = Celery(CELERY_CONFIG.name, backend=CELERY_CONFIG.backend, broker=CELERY_CONFIG.broker)

def transfer(extractor_class: type, transformer_model: pydantic.main.ModelMetaclass, index: str) -> None:
    logger.info('Запуск трансфера данных.')
    # Время последнего обновления данных в ES.
    etl_state = RedisState(settings=REDIS_CONFIG)

    # Обновленные данные в Postgres.
    raw_data = extractor_class(index=index, dsn=POSTGRES_DSN, state=etl_state).find_modified_docs()

    transformer = Transformer()
    loader = Loader(index)

    for batch in raw_data:
        # Преобразование данных для загрузки в ES.
        data_to_load, updated_at = transformer.transform_data(batch, index, transformer_model)
        # Загрузка данных в ES.
        response = loader.connector(index=index, data=data_to_load)
        # Изменение значения времени последнего обновления данных в ES.
        if response and response.status_code == HTTPStatus.OK:
            etl_state.set(f'bottom_limit_{index}', updated_at)
            
    logger.info('Трансфер данных завершен.')


@celery.task
def init_transfer():
    transfer(FilmIndex.extractor, FilmIndex.model, FilmIndex.index)
    transfer(GenreIndex.extractor, GenreIndex.model, GenreIndex.index)
    transfer(PersonIndex.extractor, PersonIndex.model, PersonIndex.index)


@celery.on_after_configure.connect
def setup_etl_periodic_task(sender, **kwargs):
    sender.add_periodic_task(
        30.0,
        init_transfer.s(),
        name='Update ETL every 30 seconds.'
    )
