import time

from elasticsearch import Elasticsearch

from ..settings import CONFIG

es = Elasticsearch(hosts=f'{CONFIG.ELASTIC.protocol}://{CONFIG.ELASTIC.host}:{CONFIG.ELASTIC.port}')


def wait_for_elastic():
    while not es.ping():
        print('Waiting for elastic...')
        time.sleep(1)

    print('Connected to elastic.')


if __name__ == '__main__':
    wait_for_elastic()
