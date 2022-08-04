import logging

import backoff
from elasticsearch import Elasticsearch

from ..settings import CONFIG

es = Elasticsearch(hosts=f'{CONFIG.ELASTIC.protocol}://{CONFIG.ELASTIC.host}:{CONFIG.ELASTIC.port}')
logger = logging.getLogger('Elasticsearch Waiter')


@backoff.on_predicate(backoff.expo, logger=logger)
def wait_for_elastic():
    return es.ping()


if __name__ == '__main__':
    wait_for_elastic()
