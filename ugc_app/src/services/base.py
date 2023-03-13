"""Base Service class handling UGC Events."""
import abc

from aiokafka import AIOKafkaProducer

from src.models import UGCEvent


class EventProducerAbstract(abc.ABC):
    @property
    @abc.abstractmethod
    def topic(self): ...

    @abc.abstractmethod
    async def send(self, *args, **kwargs): ...


class KafkaEventProducer(EventProducerAbstract):
    def __init__(self, topic: str, producer: AIOKafkaProducer) -> None:
        self._topic = topic
        self.producer = producer

    @property
    def topic(self) -> str:
        return self._topic

    async def send(self, *args, **kwargs) -> None:
        await self.producer.send(topic=self.topic, *args, **kwargs)


class EventServicerAbstract(abc.ABC):
    def __init__(self, producer: EventProducerAbstract):
        self.producer = producer

    @property
    @abc.abstractmethod
    def topic(self) -> str: ...

    @abc.abstractmethod
    async def send(self, *args, **kwargs) -> UGCEvent: ...
