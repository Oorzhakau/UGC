"""
This module contains the classes implement Cache.
"""

import abc
import json
from typing import Any
import logging

import backoff
from redis import Redis

logger = logging.getLogger(__name__)

cache: Redis | None


class CacheAbstract(abc.ABC):
    """An abstract class for cache storage."""

    @abc.abstractmethod
    def get(self, key: str, **kwargs) -> str: ...

    @abc.abstractmethod
    def set(self, key: str, value: str, expire: int, **kwargs): ...

    @abc.abstractmethod
    def expire(self, key: str, seconds: int, **kwargs) -> bool: ...

    @abc.abstractmethod
    def close(self): ...

    @abc.abstractmethod
    def delete(self, key: str | list): ...

    @abc.abstractmethod
    def keys(self, condition: str) -> list[str]: ...

    @abc.abstractmethod
    def flushall(self) -> None: ...


class RedisCache(CacheAbstract):
    """Redis cache class."""

    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    def client(self) -> Redis | None:
        return self._redis

    def get(self, key: str, **kwargs) -> str:
        data = self._redis.get(key)
        if not data:
            return
        return data.decode("ascii")

    def set(self, key: str, value: str, expire: int, **kwargs):
        self._redis.set(key, json.dumps(value), expire)

    def expire(self, key: str, seconds: int, **kwargs):
        return self._redis.expire(key, seconds, **kwargs)

    def close(self):
        self._redis.close()

    def delete(self, key: str | list):
        if isinstance(key, str):
            self._redis.delete(key)
        else:
            self._redis.delete(*key)

    def keys(self, condition: str) -> list[str]:
        return self._redis.keys(condition)

    def flushall(self) -> None:
        self._redis.flushall()


def backoff_handler(details):
    """Log backoff processing for Redis."""
    logging.error(
        'Backing off {wait:0.1f} seconds after {tries} tries '
        'calling function {target} with args {args} and kwargs '
        '{kwargs}'.format(**details),
    )


@backoff.on_exception(
    backoff.expo, (ConnectionError,),
    on_backoff=backoff_handler,
    max_time=60,
)
def create_cache(host: str, port: int) -> None:
    global cache
    cache = Redis(host=host, port=port)


def get_redis_extended() -> RedisCache:
    global cache
    return RedisCache(cache)
