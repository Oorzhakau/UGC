from typing import Optional

from src.core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient

mongo_client: Optional[AsyncIOMotorClient] = None


async def get_mongo() -> AsyncIOMotorClient:
    global mongo_client
    mongo_client = AsyncIOMotorClient(settings.mongo_uri)
    return mongo_client


async def get_mongo_client() -> AsyncIOMotorClient:
    return mongo_client

