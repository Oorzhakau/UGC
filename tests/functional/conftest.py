"""
This module stores fixtures for pytest.
"""
import asyncio

import aiohttp
import pytest
import pytest_asyncio
import requests
from aiokafka import AIOKafkaConsumer
from clickhouse_driver import Client

from tests.functional.models.response import HTTPResponse
from tests.functional.settings import settings
from tests.functional.testdata.data import test_users_data


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def kafka_consumer():
    consumer = AIOKafkaConsumer(
        "views",
        bootstrap_servers=f"{settings.KAFKA_HOST}:{settings.KAFKA_PORT}",
        enable_auto_commit=False,
        auto_offset_reset="earliest",
        group_id="ugc-group"
    )
    await consumer.start()
    yield consumer
    await consumer.stop()

@pytest.fixture(scope="session")
def clickhouse_client():
    clickhouse_client = Client(
        host=settings.CLICKHOUSE_HOST,
        port=settings.CLICKHOUSE_PORT
    )
    try:
        yield clickhouse_client
    finally:
        clickhouse_client.disconnect_connection()


@pytest_asyncio.fixture(scope='function')
async def session():
    async with aiohttp.ClientSession() as session:
        yield session
    await session.close()


@pytest_asyncio.fixture
def make_get_request(session: aiohttp.ClientSession):
    async def inner(url: str, headers: dict | None = None, query_data: str | None = None):
        async with session.get(url, params=query_data, headers=headers) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
            return HTTPResponse(body=body, headers=headers, status=status)

    return inner


@pytest_asyncio.fixture
def make_post_request(session: aiohttp.ClientSession):
    async def inner(url: str, headers: dict | None = None, data: dict | None = None):
        async with session.post(url, json=data, headers=headers) as response:
            body = await response.json()
            headers = response.headers
            status = response.status
            return HTTPResponse(body=body, headers=headers, status=status)

    return inner


@pytest.fixture(scope="session")
def registration_user():
    for user in test_users_data:
        _ = requests.post(
            url=settings.AUTH_SIGNUP_URL,
            json={
                "username": user["username"],
                "password": user["password"],
                "confirm_password": user["password"]
            }
        )
    return
