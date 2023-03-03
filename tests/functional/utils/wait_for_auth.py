"""
This module is used by Docker Compose to find out if Auth application is okay.
"""

import time
import logging.config
import os

import requests

logging.config.fileConfig(
    fname='tests/functional/log.conf',
    disable_existing_loggers=False,
)
logger = logging.getLogger(__name__)


def wait_auth_app():
    """
    Wait until Auth answers to ping(). The function is used to
    check if Auth is okay.
    """
    logger.info('Starting to check if Auth applications is up...')

    host = os.getenv('EXTERNAL_AUTH_HOST', '127.0.0.1')
    url = f"http://{host}/users/me"
    attempt = 1
    while True:
        response = requests.get(url)
        if response.status_code == 401:
            break
        else:
            time.sleep(2)
            attempt += 1
    logger.info('Auth applications is up...')


if __name__ == '__main__':
    wait_auth_app()
