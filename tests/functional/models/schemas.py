import datetime
from uuid import UUID

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class BaseOrjsonModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class TokensResponse(BaseOrjsonModel):
    access_token: str
    refresh_token: str


class RoleScheme(BaseOrjsonModel):
    id: UUID | None
    name: str
    description: str | None


class UserSignUpScheme(BaseOrjsonModel):
    name: str | None
    email: str | None
    username: str
    password: str
    confirm_password: str
