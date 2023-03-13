"""
Service handling events regarding Film View History.
"""
from functools import lru_cache

from aiokafka import AIOKafkaProducer
from fastapi import Depends

from src.models import ViewEvent, ViewEventResponse
from src.services.base import EventServicerAbstract, KafkaEventProducer
from src.db.kafka import get_producer
from src.core.config import settings


class FilmViewHistoryService(EventServicerAbstract):
    @property
    def topic(self):
        return self.producer.topic

    async def send(self, user_id: str, event: ViewEvent) -> ViewEventResponse:
        key = f"{user_id}+{event.movie_id}"
        await self.producer.send(value=str(event.progress).encode(), key=key.encode())
        return ViewEventResponse(
            user_id=user_id,
            movie_id=event.movie_id,
            progress=event.progress
        )


@lru_cache()
def get_film_view_history_service(
    producer: AIOKafkaProducer = Depends(get_producer),
) -> FilmViewHistoryService:
    event_producer = KafkaEventProducer(topic=settings.TOPIC_VIEWS, producer=producer)
    return FilmViewHistoryService(producer=event_producer)
