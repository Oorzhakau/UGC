import logging
from contextlib import contextmanager

from clickhouse_driver import Client

from settings import settings

logger = logging.getLogger(__name__)


@contextmanager
def get_clickhouse_client():
    logger.info("Creating a ClickHouse client...")
    clickhouse_client = Client(
        host=settings.CLICKHOUSE_HOST,
        port=settings.CLICKHOUSE_PORT
    )
    logger.info("Done creating a ClickHouse client...")
    try:
        yield clickhouse_client
    finally:
        clickhouse_client.disconnect_connection()
        logger.info("Close a ClickHouse client...")
