"""
Service handling events regarding Bookmark film.
"""
import logging
from functools import lru_cache
from typing import Any, List
from uuid import uuid4

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings
from src.db.mongo import get_mongo_client
from src.models.bookmark import (BookmarkEventComplete,  BookmarkEventWithUser)

logger = logging.getLogger(__name__)


class BookmarkService:
    def __init__(self, storage: AsyncIOMotorClient):
        self.storage = storage
        self.db = self.storage[settings.UGC_STORAGE_DB]
        self.collection = self.db[settings.BOOKMARKS_COLLECTION_NAME]

    async def get_bookmarks(self,
                            page_size: int,
                            page_number: int,
                            user_id: str) -> List[BookmarkEventComplete]:
        collection = self.collection
        bookmarks = []
        cursor = collection.find({"user_id": user_id})
        skip = page_size * (page_number - 1)
        cursor.sort("dt", -1).skip(skip).limit(page_size)
        async for bookmark in collection.find({"user_id": user_id}):
            bookmark["id"] = bookmark.pop("_id")
            bookmarks.append(BookmarkEventComplete(**bookmark))
        return bookmarks

    async def add_bookmark(self, bookmark: BookmarkEventWithUser) -> Any:
        bookmark_payload = bookmark.dict()
        bookmark_payload["_id"] = str(uuid4())
        bookmark = await self.collection.insert_one(bookmark_payload)
        return bookmark.inserted_id

    async def delete_bookmark(self, bookmark_id: str, user_id: str) -> None:
        await self.collection.delete_one({"_id": bookmark_id, "user_id": user_id})


@lru_cache()
def get_bookmark_service(
    mongo_storage: AsyncIOMotorClient = Depends(get_mongo_client),
) -> BookmarkService:
    return BookmarkService(storage=mongo_storage)
