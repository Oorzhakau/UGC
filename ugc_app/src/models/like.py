"""Like model."""
from datetime import datetime

from pydantic import Field

from src.models.base import BaseOrjsonModel


class MovieLikeEvent(BaseOrjsonModel):
    movie_id: str
    rating: int = Field(ge=0, le=10)


class MovieLikeEventWithUser(MovieLikeEvent):
    user_id: str
    dt: datetime = datetime.now()


class ReviewLikeEvent(BaseOrjsonModel):
    review_id: str
    rating: int = Field(ge=0, le=10)


class ReviewLikeEventWithUser(ReviewLikeEvent):
    user_id: str
    dt: datetime = datetime.now()

