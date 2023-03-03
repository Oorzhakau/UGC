"""
This module is used by Docker Compose to find out if Redis is okay.
"""

import time
import logging.config
import os

from redis import Redis
from redis.exceptions import ConnectionError


logging.config.fileConfig(
    fname=os.path.join(os.getcwd(), "log.conf"),
    disable_existing_loggers=False,
)
logger = logging.getLogger(__name__)


def wait_redis():
    """
    Wait until Redis answers to ping(). The function is used to
    check if Redis is okay.
    """
    logger.info("Starting to check if Redis is up...")

    host = os.getenv("AUTH_REDIS_HOST", default="127.0.0.1")
    port = os.getenv("AUTH_REDIS_PORT", default="6379")
    attempt = 1
    while True:
        try:
            logger.info(f"Trying to ping Redis (attempt {attempt})...")
            redis = Redis(host=host, port=int(port), db=0)
            _ = redis.ping()
            break
        except (ConnectionError, ConnectionRefusedError):
            time.sleep(2)
            attempt += 1
    logger.info("Redis is up...")


if __name__ == "__main__":
    wait_redis()
