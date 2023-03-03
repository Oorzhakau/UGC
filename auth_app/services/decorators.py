from datetime import datetime
from functools import wraps
from http import HTTPStatus

from flask import abort, jsonify, make_response, request
from flask_jwt_extended import current_user, decode_token, get_jwt
from flask_jwt_extended.exceptions import JWTDecodeError
from jwt.exceptions import DecodeError

from db.cache_factory import cache
from enumeration import Errors
from services.user_service import get_user_service
from settings.config import settings


def access_permission_jwt(roles: list[str]):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            claim_roles = get_jwt()['roles']
            if not set(claim_roles).intersection(roles):
                return Errors.permission_denied
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


def write_to_accout_history(action: str):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            service = get_user_service()
            service.add_action_in_history(
                user=current_user,
                user_agent=request.headers.get('User-Agent'),
                action=action
            )
            return fn(*args, **kwargs)

        return decorated_view

    return wrapper


def rate_limit(func):
    """
    Декоратор реализации ограничения количества запросов в минуту для
    соответствующего api метода. При наличии корректного токена ограничение
    привязывается к токену, а при его отсутствие - к ip клиента.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        pipe = cache.pipeline()
        now = datetime.now()
        preffix = request.headers.get("Authorization")
        try:
            _ = decode_token(preffix, allow_expired=False)
        except (JWTDecodeError, DecodeError):
            preffix = None
        if not preffix:
            preffix = request.remote_addr
        key = f'{preffix}:{now.minute}'
        pipe.incr(key, 1)
        pipe.expire(key, 59)
        result = pipe.execute()
        request_number = result[0]
        if request_number > settings.RATE_LIMIT_REQ_PER_MIN:
            abort(make_response(jsonify(message="Too many requests per minute"), HTTPStatus.TOO_MANY_REQUESTS))
        result = func(*args, **kwargs)
        return result

    return wrapper
