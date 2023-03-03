import logging
import time
import uuid

import backoff as backoff
from clickhouse_driver import Client
from clickhouse_driver.errors import Error
from kafka import KafkaConsumer, TopicPartition, OffsetAndMetadata
from kafka.errors import NoBrokersAvailable, KafkaError

from settings import settings

from clickhouse_init import get_clickhouse_client
from kafka_init import get_kafka_consumer


logger = logging.getLogger(__name__)

MESSAGE_COUNT = settings.MESSAGE_COUNT


def create_table(client) -> None:
    """
    Creating table in ClickHouse
    :param client: ClickHouse connection
    """
    logger.info('Creating a ClickHouse table...')
    client.execute(
        """CREATE TABLE IF NOT EXISTS views (
            id String,
            user_id String,
            movie_id String,
            timestamp_movie Int64,
            progress Int64
            ) Engine=MergeTree() ORDER BY id
        """
    )
    logger.info('Done creating a ClickHouse table')


@backoff.on_exception(backoff.expo, Exception, max_tries=3)
def insert_in_clickhouse(client, data: list) -> None:
    """
    Inserting data in ClickHouse
    :param client: ClickHouse connection
    :param data: Data for load
    """
    logger.info('Inserting data into ClickHouse...')
    for i in data:
        logger.info(f'Inserting {i} into ClickHouse...')
        client.execute(
            f'''
            INSERT INTO views (
            id, user_id, movie_id, timestamp_movie, progress)  VALUES {i}
            '''
        )
        logger.info(f'Done inserting {i} into ClickHouse')
    logger.info('Done inserting data into ClickHouse')


def etl(consumer: KafkaConsumer, clickhouse_client: Client) -> None:
    data = []
    logger.info('Stating an ETL pipeline...')
    for message in consumer:
        logger.info(f'Processing message {message}...')
        uuid_ = str(uuid.uuid4())
        user_id, movie_id = message.key.decode('utf-8').split('+')
        progress = message.value
        timestamp = message.timestamp
        msg = (uuid_, user_id, movie_id, progress, timestamp)
        data.append(msg)

        if len(data) == MESSAGE_COUNT:
            insert_in_clickhouse(clickhouse_client, data)
            data.clear()
            tp = TopicPartition(settings.KAFKA_BROKER_TOPIC, message.partition)
            options = {tp: OffsetAndMetadata(message.offset + 1, None)}
            consumer.commit(options)
        logger.info(f'Done processing message {message}...')


@backoff.on_exception(backoff.expo, (NoBrokersAvailable, Error))
def main() -> None:
    with get_clickhouse_client() as clickhouse_client, get_kafka_consumer() as consumer:
        create_table(clickhouse_client)
        while True:
            try:
                etl(consumer, clickhouse_client)
            except (KafkaError, Error) as err:
                logger.error("Got unexpected error: {}.".format(err))
            finally:
                time.sleep(settings.SLEEP_TIME)


if __name__ == '__main__':
    main()
