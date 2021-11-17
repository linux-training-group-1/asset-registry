import json

import redis
import os

r = None


def redis_conn():
    global r
    if r is None:
        pool = redis.ConnectionPool(host=os.environ['REDIS_HOST'],
                                    port=os.environ['REDIS_PORT'],
                                    db=int(os.environ['REDIS_DB']))
        r = redis.Redis(connection_pool=pool)
    return r


def set_cache_item_json(key, item):
    redis_conn()
    # Convert python dict to JSON str and save to Redis
    item = json.dumps(item)
    r.set(key, item)


def get_cache_item_json(key):
    redis_conn()
    return json.loads(r.get(key))
