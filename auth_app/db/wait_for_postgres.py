"""
This module is used by Docker Compose to find out if Elasticsearch is okay.
"""

import logging.config
import os
import time

import psycopg2

logging.config.fileConfig(
    fname=os.path.join(os.getcwd(), "log.conf"),
    disable_existing_loggers=False,
)
logger = logging.getLogger(__name__)


def wait_postgres():
    host = os.getenv("AUTH_POSTGRES_DB_HOST", default="127.0.0.1")
    port = os.getenv("AUTH_POSTGRES_DB_PORT", default="5432")
    user = os.getenv("AUTH_POSTGRES_USER", default="app")
    password = os.getenv("AUTH_POSTGRES_PASSWORD", default="123qwe")
    database = os.getenv("AUTH_POSTGRES_DB", default="auth_db")
    logger.info("Starting to check if Postgres DB is up...")
    attempt = 1
    while True:
        logger.info(f"Trying to ping Postgres (attempt {attempt})...")
        try:
            conn = psycopg2.connect(
                host=host, port=port, database=database, user=user, password=password
            )
            conn.close()
            break
        except psycopg2.OperationalError:
            time.sleep(2)
            attempt += 1
    logger.info("Postgres is up!")


if __name__ == "__main__":
    wait_postgres()
