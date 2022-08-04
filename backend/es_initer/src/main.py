import json

from config.base import ELASTIC_CONFIG, ELASTIC_INDICES
from elastic_initer import ElasticIniter

if __name__ == '__main__':
    es_initer = ElasticIniter(settings=ELASTIC_CONFIG)

    indices = list(ELASTIC_INDICES.dict().values())

    for index_name in indices:
        mapping = None

        with open(f'./mapping/{index_name}.json', 'r') as fd:
            mapping = json.load(fd)

        es_initer.create(index_name=index_name, mapping=mapping)
