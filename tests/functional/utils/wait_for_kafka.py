"""
This module is used by Docker Compose to find out if Kafka is okay.
"""

import time
import logging.config
import os

import kafka
from kafka.errors import NoBrokersAvailable

logging.config.fileConfig(
    fname='tests/functional/log.conf',
    disable_existing_loggers=False,
)
logger = logging.getLogger(__name__)


def wait_kafka():
    """
    Wait until Kafka answers to ping(). The function is used to
    check if Kafka is okay.
    """
    logger.info('Starting to check if Kafka is up...')

    host = os.getenv('KAFKA_BROKER_HOST', '127.0.0.1')
    port = os.getenv('KAFKA_BROKER_EXTERNAL_PORT', '9092')
    attempt = 1
    while True:
        try:

            consumer = kafka.KafkaConsumer(
                group_id='test',
                bootstrap_servers=[f'{host}:{port}'],
                auto_offset_reset='earliest',
            )
            topics = consumer.topics()
            if not topics:
                raise NoBrokersAvailable
            break
        except (NoBrokersAvailable,):
            time.sleep(2)
            attempt += 1
    logger.info('Kafka is up...')


if __name__ == '__main__':
    wait_kafka()
