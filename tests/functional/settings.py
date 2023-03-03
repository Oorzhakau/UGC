from logging import config as logging_config

from pydantic import BaseSettings, Field

from tests.functional.utils.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    """The class contains settings for the project."""
    PROJECT_NAME = Field('auth', env='UGC_PROJECT_NAME')
    AUTH_SIGNUP_URL: str = Field('http://127.0.0.1:80/users/signup', env='AUTH_SIGNUP_URL')
    AUTH_LOGIN_URL: str = Field('http://127.0.0.1:80/users/login', env='AUTH_LOGIN_URL')
    UGC_URL: str = Field('http://127.0.0.1:8010/ugc/api/v1/views/', env='UGC_URL')

    DEBUG: str = Field('True', env='DEBUG')

    DB: str = Field('postgresql', env='AUTH_DB')
    DB_USER: str = Field('app', env='AUTH_POSTGRES_USER')
    DB_PASSWORD: str = Field('123qwe', env='AUTH_POSTGRES_PASSWORD')
    DB_HOST: str = Field('127.0.0.1', env='AUTH_POSTGRES_DB_HOST')
    DB_PORT: int = Field(5432, env='AUTH_POSTGRES_DB_PORT')
    DB_NAME: str = Field('auth_db', env='AUTH_POSTGRES_DB')

    KAFKA_HOST: str = Field('127.0.0.1', env='KAFKA_BROKER_HOST')
    KAFKA_PORT: int = Field(9092, env='KAFKA_BROKER_PORT')

    CLICKHOUSE_HOST: str = Field('127.0.0.1', env='CLICKHOUSE_HOST')
    CLICKHOUSE_PORT: int = Field(9000, env='CLICKHOUSE_PORT_ZOOKEPEER')

    ETL_SLEEP_TIME: int = Field(5, env='ETL_SLEEP_TIME')


settings = Settings()
