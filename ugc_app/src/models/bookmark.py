"""Bookmark model."""
from pydantic import Field

from src.models.base import BaseOrjsonModel, UGCEvent


class BookmarkEvent(BaseOrjsonModel):
    movie_id: str


class BookmarkEventWithUser(BookmarkEvent, UGCEvent):
    user_id: str


class BookmarkEventComplete(BookmarkEventWithUser):
    id: str = Field(alias="_id")
