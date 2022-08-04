import logging

import backoff
from redis import ConnectionError, Redis

from ..settings import CONFIG

r = Redis(CONFIG.REDIS.host)
logger = logging.getLogger('Redis Waiter')


@backoff.on_predicate(backoff.expo, logger=logger)
def wait_for_redis():
    try:
        r.ping()
        return True
    except ConnectionError:
        return False


if __name__ == '__main__':
    wait_for_redis()
