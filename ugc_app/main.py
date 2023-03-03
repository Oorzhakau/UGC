from aiokafka import AIOKafkaProducer
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
import uvicorn
import sentry_sdk

from src.api.v1 import events
from src.db import event_storage
from src.core.config import settings

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

app.include_router(
    events.router,
    prefix="/ugc/api/v1/views",
    tags=["ugc"]
)


@app.on_event("startup")
async def startup() -> None:
    event_storage.event_producer = AIOKafkaProducer(
        **{
            'bootstrap_servers': '{}:{}'.format(settings.KAFKA_BROKER_HOST, settings.KAFKA_BROKER_PORT)
        }
    )
    await event_storage.event_producer.start()


@app.on_event("shutdown")
async def shutdown() -> None:
    await event_storage.event_producer.stop()


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8001)
