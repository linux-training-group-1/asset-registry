import json
import os
from difflib import SequenceMatcher

import redis

_pool = None

string_similarity_score = 0.7
cache_expire_seconds = 3600


def _redis_conn():
    # Singleton connection pool
    global _pool
    if _pool is None:
        _pool = redis.ConnectionPool(host=os.environ['REDIS_HOST'],
                                     port=os.environ['REDIS_PORT'],
                                     db=int(os.environ['REDIS_DB']))
    r = redis.Redis(connection_pool=_pool)
    return r


def set_cache_item_json(key, item):
    r = _redis_conn()
    # Convert python dict to JSON str and save to Redis
    item = json.dumps(item)
    r.set(key, item, ex=cache_expire_seconds)


def get_cache_item_json(key):
    r = _redis_conn()
    return json.loads(r.get(key))


def _string_match(source, keyword):
    if keyword == source:
        return True
    elif keyword in source:
        return True
    return SequenceMatcher(None, source, keyword).ratio() > string_similarity_score


def string_search(keyword):
    r = _redis_conn()
    results = []
    for key in r.scan_iter():
        key = key.decode("utf-8")
        val = r.get(key).decode("utf-8")
        # print(key, keyword)
        if _string_match(key, keyword):
            # identify json objects
            try:
                obj_parsed = json.loads(val)
                # print(obj_parsed)
                results.append(obj_parsed)
            except ValueError:
                # Not a json object, do nothing
                pass
    return results
