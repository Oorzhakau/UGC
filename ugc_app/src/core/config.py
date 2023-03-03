import os
from logging import config as logging_config
from typing import Optional

from dotenv import find_dotenv
from pydantic import BaseSettings, Field

from src.core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    """The class contains settings for the project."""

    BASE_DIR = Field(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DEBUG: str = Field("False", env="DEBUG")

    KAFKA_ZOOKEPEER_HOST: str = Field(default="127.0.0.1", env="UGC_ZOOKEPEER_HOST")
    KAFKA_ZOOKEPEER_PORT: int = Field(default=2181, env="UGC_ZOOKEPEER_PORT")

    KAFKA_BROKER_HOST: str = Field(default="127.0.0.1", env="KAFKA_BROKER_HOST")
    KAFKA_BROKER_PORT: int = Field(default=9092, env="KAFKA_BROKER_PORT")

    PROJECT_NAME = Field("UGC", env="UGC_PROJECT_NAME")

    AUTH_PROJECT_HOST: str = Field(default="127.0.0.1", env="EXTERNAL_AUTH_HOST")
    AUTH_PROJECT_PORT: int = Field(default=80, env="EXTERNAL_AUTH_PORT")
    AUTH_PROJECT_SLUG: str = Field(default="users/verification_roles")

    ROLES: list[str] = Field(["admin", "base", "extended", "manager"])

    TOPIC_VIEWS = "views"

    UGC_DSC: Optional[str] = Field(env="UGC_DSC")

    class Config:
        env_file = find_dotenv(filename=".env", usecwd=True)
        env_file_encoding = 'utf-8'


settings = Settings()
