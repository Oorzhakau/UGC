import functools
from http import HTTPStatus

import aiohttp
from fastapi import Request, HTTPException

from src.core.config import settings

URL = (
    f"http://{settings.AUTH_PROJECT_HOST}"
    f":{settings.AUTH_PROJECT_PORT}"
    f"/{settings.AUTH_PROJECT_SLUG}"
)


async def auth_request(session, token):
    async with session.get(URL, headers={"Authorization": token}) as response:
        status = response.status
        response_body = await response.json()
        return {"status": status, "body": response_body}


def access_check(
    assigned_roles: list[str] = settings.ROLES,
):
    """A decorator for check access to api handler."""

    def wrap(fn):
        @functools.wraps(fn)
        async def decorated(request: Request, **kwargs):
            token = request.headers.get("Authorization")
            scope = request.scope
            try:
                async with aiohttp.ClientSession() as session:
                    response = await auth_request(session, token)
                if response["status"] == HTTPStatus.OK:
                    response_role = response["body"]["roles"]
                else:
                    response_role = ["anonymous"]
            except Exception:
                response_role = ["anonymous"]

            if not list(set(response_role) & set(assigned_roles)):
                raise HTTPException(
                    status_code=HTTPStatus.FORBIDDEN,
                    detail="You don't have permissions for this api method",
                )
            data = await fn(Request(scope, response["body"]["user_id"]), **kwargs)
            return data

        return decorated

    return wrap
