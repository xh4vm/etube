import time

from redis import ConnectionError, Redis

from ..settings import CONFIG

r = Redis(CONFIG.REDIS.host)


def wait_for_redis():
    while True:
        try:
            r.ping()
            break
        except ConnectionError:
            print('Waiting for redis...')
            time.sleep(1)

    print('Connected to redis.')


if __name__ == '__main__':
    wait_for_redis()
