import datetime
from uuid import UUID

import orjson
from pydantic import BaseModel, root_validator, validator, EmailStr

from settings.config import settings


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


class RolesRequest(BaseOrjsonModel):
    roles: list[str]


class UserSignInScheme(BaseOrjsonModel):
    username: str
    password: str


class UserSignUpScheme(BaseOrjsonModel):
    name: str | None
    email: str | None
    username: str
    password: str
    confirm_password: str
    roles: list[RoleScheme] | None

    @validator('password')
    def check_storage_type(cls, value):
        if len(value) < 8:
            raise ValueError('Password must have at least 8 characters.')
        return value

    @root_validator()
    def verify_password_match(cls, values):
        password = values.get('password')
        confirm_password = values.get('confirm_password')

        if password != confirm_password:
            raise ValueError('The two passwords did not match.')
        return values


class AccountScheme(BaseOrjsonModel):
    id: UUID | None
    name: str | None
    email: EmailStr | None
    username: str | None
    roles: list[RoleScheme] | None


class PasswordChange(BaseOrjsonModel):
    curr_password: str
    new_password: str
    confirm_password: str

    @root_validator()
    def validate_password(cls, values):
        curr_pass = values.get('curr_password')
        new_pass = values.get('new_password')
        confirm_pass = values.get('confirm_password')
        if len(new_pass) < 8:
            raise ValueError('Password must have at least 8 characters')
        elif new_pass == curr_pass:
            raise ValueError('New password must not be equal old password')
        elif confirm_pass != new_pass:
            raise ValueError('Confirm password not valid')
        return values


class AccountHistory(BaseOrjsonModel):
    id: UUID
    created: datetime.datetime
    user_agent: str | None
    device: str | None
    action: str | None


class UserReduce(BaseOrjsonModel):
    user_id: UUID
    roles: list[str]


class Pagination(BaseOrjsonModel):
    page: int = settings.PAGE
    per_page: int = settings.PER_PAGE

    @root_validator()
    def validate_password(cls, values):
        page = values.get('page')
        per_page = values.get('per_page')
        if page < 1 or per_page < 0:
            raise ValueError('Invalid parameters pagination')
        return values


class PaginationResponse(BaseOrjsonModel):
    page: int
    pages: int
    total: int
    prev_page: int | None
    next_page: int | None
    has_next: bool | None
    has_prev: bool | None
    results: list
