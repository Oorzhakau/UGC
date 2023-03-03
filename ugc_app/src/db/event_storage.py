from typing import Optional

from aiokafka import AIOKafkaProducer

event_producer: Optional[AIOKafkaProducer] = None


def get_producer() -> Optional[AIOKafkaProducer]:
    return event_producer
