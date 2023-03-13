"""View model."""
from src.models.base import UGCEvent


class ViewEvent(UGCEvent):
    movie_id: str
    progress: int


class ViewEventResponse(UGCEvent):
    user_id: str
    movie_id: str
    progress: int
