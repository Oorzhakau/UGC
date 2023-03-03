"""
This module is used by Docker Compose to find out if Clickhouse is okay.
"""

import time
import logging.config
import os

from clickhouse_driver import Client
import requests

logging.config.fileConfig(
    fname='tests/functional/log.conf',
    disable_existing_loggers=False,
)
logger = logging.getLogger(__name__)


def wait_ch():
    """
    Wait until Clickhouse answers to ping(). The function is used to
    check if Clickhouse is okay.
    """
    logger.info('Starting to check if Clickhouse is up...')

    host = os.getenv('CLICKHOUSE_HOST', '127.0.0.1')
    port = os.getenv('CLICKHOUSE_PORT_BASE', '8123')
    url = f"http://{host}:{port}/ping"
    attempt = 1
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            break
        else:
            time.sleep(2)
            attempt += 1
    logger.info('Clickhouse is up...')


if __name__ == '__main__':
    wait_ch()
