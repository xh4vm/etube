import backoff
from elasticsearch import Elasticsearch

from ..settings import CONFIG

es = Elasticsearch(hosts=f'{CONFIG.ELASTIC.protocol}://{CONFIG.ELASTIC.host}:{CONFIG.ELASTIC.port}')


@backoff.on_predicate(backoff.expo)
def wait_for_elastic():
    return es.ping()


if __name__ == '__main__':
    wait_for_elastic()
