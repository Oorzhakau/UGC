import logging

import backoff
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

logger = logging.getLogger(__name__)

db: SQLAlchemy | None = None


def backoff_handler(details):
    """Log backoff processing for Postgresql."""
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
def create_db(app: Flask):
    global db
    db = SQLAlchemy(app)
    Migrate(app, db)


def get_db() -> SQLAlchemy:
    return db
