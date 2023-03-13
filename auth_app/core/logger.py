import logging

from flask import request
from logstash import LogstashHandler

LOG_FORMAT = 'auth_app:  %(asctime)s - %(name)s - %(levelname)s - %(message)s'


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request.headers.get('X-Request-Id')
        return True


def init_logstash(app, settings):
    logstash_handler = LogstashHandler(
        settings.LOGSTASH_HOST,
        int(settings.LOGSTASH_PORT),
        version=1,
        tags=["auth_app"]
    )
    logstash_handler.setLevel(logging.INFO)
    logstash_handler.addFilter(RequestIdFilter())
    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(logstash_handler)
    return app
