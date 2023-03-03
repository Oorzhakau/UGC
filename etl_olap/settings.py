from pydantic import BaseSettings,  Field


class Settings(BaseSettings):
    KAFKA_BROKER_HOST: str = Field(default='localhost', env='KAFKA_BROKER_HOST')
    KAFKA_BROKER_PORT: int = Field(default=9092, env='KAFKA_BROKER_EXTERNAL_PORT')
    KAFKA_BROKER_TOPIC: str = Field(default='views', env='KAFKA_BROKER_TOPIC')

    CLICKHOUSE_HOST: str = Field(default='localhost', env='CLICKHOUSE_HOST')
    CLICKHOUSE_PORT: str = Field(default=9000, env='CLICKHOUSE_PORT_ZOOKEPEER')

    MESSAGE_COUNT: int = 1
    SLEEP_TIME = Field(default=5, env='ETL_SLEEP_TIME')


settings = Settings()
