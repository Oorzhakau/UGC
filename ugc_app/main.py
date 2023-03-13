import logging

import logstash
import sentry_sdk
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api.v1 import bookmarks, likes, reviews, views
from src.core.config import settings
from src.core.logger import LOGGING
from src.db import kafka, mongo

sentry_sdk.init(
    dsn=settings.UGC_DSC,
    traces_sample_rate=1.0,
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url='/ugc/api/openapi',
    openapi_url='/ugc/api/openapi.json',
    default_response_class=ORJSONResponse,
)

logger = logging.getLogger("ugc_app")
logger.setLevel(logging.INFO)
logger.addHandler(
    logstash.LogstashHandler(
        settings.LOGSTASH_HOST,
        int(settings.LOGSTASH_PORT),
        version=1,
        tags=["ugc_app"]
    )
)


@app.on_event("startup")
async def startup() -> None:
    logger.info("Start ugc_app!")
    await kafka.init_producer()
    await mongo.get_mongo()


@app.on_event("shutdown")
async def shutdown() -> None:
    await kafka.event_producer.stop()
    mongo.get_mongo().close()


app.include_router(bookmarks.router, prefix="/ugc/api/v1")
app.include_router(likes.router, prefix="/ugc/api/v1")
app.include_router(reviews.router, prefix="/ugc/api/v1")
app.include_router(views.router, prefix="/ugc/api/v1")

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', log_config=LOGGING, log_level=logging.DEBUG, port=8001)
