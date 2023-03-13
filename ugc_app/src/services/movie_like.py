"""
Service handling events regarding Like film.
"""
import logging
from functools import lru_cache

from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends

from src.core.config import settings
from src.db.mongo import get_mongo_client
from src.models.like import MovieLikeEventWithUser, ReviewLikeEventWithUser

logger = logging.getLogger(__name__)


class LikeService:
    def __init__(self, storage: AsyncIOMotorClient):
        self.storage = storage
        self.db = self.storage[settings.UGC_STORAGE_DB]

    async def add_review_like(self, like: ReviewLikeEventWithUser) -> str:
        collection = self.db[settings.REVIEW_LIKES_COLLECTION_NAME]
        await collection.delete_one(
            {"review_id": like.review_id, "user_id": like.user_id}
        )
        like = await collection.insert_one(like.dict())
        return like.inserted_id

    async def delete_review_like(self, review_id: str, user_id: str) -> None:
        collection = self.db[settings.MOVIE_LIKES_COLLECTION_NAME]
        await collection.delete_one({"review_id": review_id, "user_id": user_id})

    async def add_movie_like(self, like: MovieLikeEventWithUser) -> MovieLikeEventWithUser:
        collection = self.db[settings.MOVIE_LIKES_COLLECTION_NAME]
        await collection.find_one_and_replace(
            {"movie_id": like.movie_id, "user_id": like.user_id}, like.dict(), upsert=True
        )
        return like

    async def delete_movie_like(self, movie_id: str, user_id: str) -> None:
        collection = self.db[settings.MOVIE_LIKES_COLLECTION_NAME]
        await collection.delete_one({"movie_id": movie_id, "user_id": user_id})

    async def get_avg_review_rating(self, review_id: str) -> float | None:
        collection = self.db[settings.REVIEW_LIKES_COLLECTION_NAME]
        pipeline = [
            {"$match": {"review_id": review_id}},
            {"$group": {"_id": "_id", "avg_rating": {"$avg": "$rating"}}}
        ]
        results = []
        async for result in collection.aggregate(pipeline):
            results.append(result)
        if results:
            rating = round(results[0]["avg_rating"], 2)
        else:
            rating = None
        return rating

    async def get_avg_movie_rating(self, movie_id: str) -> float | None:
        collection = self.db[settings.MOVIE_LIKES_COLLECTION_NAME]
        pipeline = [
            {"$match": {"movie_id": movie_id}},
            {"$group": {"_id": "_id", "avg_rating": {"$avg": "$rating"}}}
        ]
        results = []
        async for result in collection.aggregate(pipeline):
            results.append(result)
        if results:
            rating = round(results[0]["avg_rating"], 2)
        else:
            rating = None
        return rating


@lru_cache()
def get_like_service(
    mongo_storage: AsyncIOMotorClient = Depends(get_mongo_client),
) -> LikeService:
    return LikeService(storage=mongo_storage)
