"""
Service handling events regarding Review film History.
"""
import logging
from functools import lru_cache
from uuid import uuid4

from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends

from src.core.config import settings
from src.db.mongo import get_mongo_client

from src.models.review import ReviewEventWithUser, ReviewEventComplete

logger = logging.getLogger(__name__)


class ReviewService:
    def __init__(self, storage: AsyncIOMotorClient):
        self.storage = storage
        self.db = self.storage[settings.UGC_STORAGE_DB]
        self.collection = self.db[settings.REVIEWS_COLLECTION_NAME]

    async def add_review(self, review: ReviewEventWithUser) -> ReviewEventComplete:
        review_dict = review.dict()
        await self.collection.delete_one(
            {"movie_id": review.movie_id, "user_id": review.user_id}
        )
        review_dict["_id"] = str(uuid4())
        await self.collection.insert_one(review_dict)
        review_dict["id"] = review_dict["_id"]
        review = ReviewEventComplete(**review_dict)
        return review

    async def get_reviews(self,
                          page_size: int,
                          page_number: int,
                          movie_id: str) -> list[ReviewEventComplete]:
        collection = self.db[settings.REVIEWS_COLLECTION_NAME]
        reviews = []
        cursor = collection.find({"movie_id": movie_id})
        skip = page_size * (page_number - 1)
        cursor.sort("dt", -1).skip(skip).limit(page_size)
        async for review in cursor:
            review["id"] = review["_id"]
            reviews.append(ReviewEventComplete(**review))
        return reviews

    async def get_user_reviews(self,
                               skip: int,
                               limit: int,
                               user_id: str) -> list[ReviewEventComplete]:
        reviews = []
        cursor = self.collection.find({"user_id": user_id})
        cursor.sort("dt", -1).skip(skip).limit(limit)
        async for review in cursor:
            review["id"] = review["_id"]
            reviews.append(ReviewEventComplete(**review))
        return reviews


@lru_cache()
def get_review_service(
        mongo_storage: AsyncIOMotorClient = Depends(get_mongo_client),
) -> ReviewService:
    return ReviewService(storage=mongo_storage)
