from typing import Optional

from aiokafka import AIOKafkaProducer

from src.core.config import settings

event_producer: Optional[AIOKafkaProducer] = None


async def init_producer() -> None:
    global event_producer
    event_producer = AIOKafkaProducer(
        **{
            'bootstrap_servers': '{}:{}'.format(
                settings.KAFKA_BROKER_HOST, settings.KAFKA_BROKER_PORT
            )
        }
    )
    await event_producer.start()


def get_producer() -> Optional[AIOKafkaProducer]:
    return event_producer
