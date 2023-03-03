from aiokafka import AIOKafkaProducer

event_producer: AIOKafkaProducer | None = None


def get_producer() -> AIOKafkaProducer | None:
    return event_producer
