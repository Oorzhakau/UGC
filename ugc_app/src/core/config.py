import os
from typing import Optional

from dotenv import find_dotenv
from pydantic import BaseSettings, Field


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

    LOGSTASH_HOST: str = "127.0.0.1"
    LOGSTASH_PORT: int = 5044

    UGC_STORAGE_HOST: str = "127.0.0.1"
    UGC_STORAGE_PORT: int = 27017
    UGC_STORAGE_DB: str = "ugc_db"

    BOOKMARKS_COLLECTION_NAME: str = "movie_bookmarks"
    REVIEWS_COLLECTION_NAME: str = "movie_reviews"
    MOVIE_LIKES_COLLECTION_NAME: str = "movie_likes"
    REVIEW_LIKES_COLLECTION_NAME: str = "review_likes"

    class Config:
        env_file = find_dotenv(filename=".env", usecwd=True)
        env_file_encoding = 'utf-8'

    @property
    def mongo_uri(self) -> str:
        return f"mongodb://{self.UGC_STORAGE_HOST}:{self.UGC_STORAGE_PORT}"

    def get_collections(self) -> list[str]:
        return [
            self.BOOKMARKS_COLLECTION_NAME,
            self.REVIEWS_COLLECTION_NAME,
            self.MOVIE_LIKES_COLLECTION_NAME,
            self.REVIEW_LIKES_COLLECTION_NAME
        ]


settings = Settings()
