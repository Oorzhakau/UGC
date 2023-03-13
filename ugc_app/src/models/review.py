"""Review model."""
from datetime import datetime

from pydantic import Field

from src.models.base import BaseOrjsonModel


class ReviewEvent(BaseOrjsonModel):
    movie_id: str
    review: str
    rating: int = Field(ge=0, le=10)


class ReviewEventWithUser(ReviewEvent):
    user_id: str
    dt: datetime = datetime.now()


class ReviewEventComplete(ReviewEventWithUser):
    id: str

    class Config:
        allow_population_by_field_name = True
        response_model_by_alias = True
