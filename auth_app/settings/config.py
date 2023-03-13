from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """The class contains settings for the project."""

    PROJECT_NAME = Field("auth", env="AUTH_PROJECT_NAME")
    PROJECT_HOST: str = Field("127.0.0.1", env="AUTH_PROJECT_HOST")
    PROJECT_PORT: int = Field(5000, env="AUTH_PROJECT_PORT")
    PROJECT_SECRET: str = Field("secret-key", env="AUTH_PROJECT_SECRET_KEY")

    JWT_SECRET: str = Field("secret-key", env="AUTH_FLASK_PORT")

    DEBUG: str = Field("True", env="AUTH_DEBUG")

    REDIS_HOST: str = Field("127.0.0.1", env="AUTH_REDIS_HOST")
    REDIS_PORT: int = Field(6379, env="AUTH_REDIS_PORT")

    ACCESS_TOKEN_EXPIRE: int = Field(600, env="AUTH_ACCESS_TOKEN_EXPIRED_SEC")
    REFRESH_TOKEN_EXPIRE: int = Field(864000, env="AUTH_REFRESH_TOKEN_EXPIRE")

    DB: str = Field("postgresql", env="AUTH_DB")
    DB_USER: str = Field("app", env="AUTH_POSTGRES_USER")
    DB_PASSWORD: str = Field("123qwe", env="AUTH_POSTGRES_PASSWORD")
    DB_HOST: str = Field("127.0.0.1", env="AUTH_POSTGRES_DB_HOST")
    DB_PORT: int = Field(5432, env="AUTH_POSTGRES_DB_PORT")
    DB_NAME: str = Field("auth_db", env="AUTH_POSTGRES_DB")

    GOOGLE_CLIENT_ID: str = Field("client", env="AUTH_GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = Field("client", env="AUTH_GOOGLE_CLIENT_SECRET")
    GOOGLE_SERVER_METADATA_URL: str = (
        "https://accounts.google.com/.well-known/openid-configuration"
    )
    GOOGLE_CLIENT_KWARGS: dict = {"scope": "openid email profile"}

    YANDEX_CLIENT_ID: str = Field("client", env="AUTH_YANDEX_CLIENT_ID")
    YANDEX_CLIENT_SECRET: str = Field("client", env="AUTH_YANDEX_CLIENT_SECRET")
    YANDEX_API_BASE_URL: str = "https://login.yandex.ru/"
    YANDEX_AUTHORIZE_URL: str = "https://oauth.yandex.com/authorize"
    YANDEX_ACCESS_TOKEN_URL: str = "https://oauth.yandex.com/token"

    JAEGER_ACTIVATE: bool = Field(False, env="JAEGER_ACTIVATE")
    JAEGER_HOSTNAME: str = Field("127.0.0.1", env="JAEGER_HOSTNAME")
    JAEGER_PORT: int = Field(6831, env="JAEGER_PORT")

    PAGE: int = 1
    PER_PAGE: int = 20

    RATE_LIMIT_REQ_PER_MIN: int = Field(20, env="RATE_LIMIT_REQ_PER_MIN")

    LOGSTASH_HOST: str = Field("127.0.0.1", env="LOGSTASH_HOST")
    LOGSTASH_PORT: int = 5044

    class Config:
        env_file = '.env.prod', '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
