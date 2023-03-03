import json
import logging
from contextlib import contextmanager

from kafka import KafkaConsumer
from settings import settings

logger = logging.getLogger(__name__)


@contextmanager
def get_kafka_consumer():
    logger.info("Creating a Kafka Consumer...")
    consumer = KafkaConsumer(
        settings.KAFKA_BROKER_TOPIC,
        group_id="movies",
        bootstrap_servers=f"{settings.KAFKA_BROKER_HOST}:{settings.KAFKA_BROKER_PORT}",
        enable_auto_commit=False,
        auto_offset_reset="earliest",
        value_deserializer=lambda x: json.loads(x.decode()),
        consumer_timeout_ms=1000
    )
    logger.info("Done creating a Kafka Consumer...")
    try:
        yield consumer
    finally:
        consumer.close()
        logger.info("Close a Kafka Consumer...")
