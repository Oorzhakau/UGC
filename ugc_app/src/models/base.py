"""
Base UGC model storage
"""
from datetime import datetime

import orjson
from pydantic import BaseModel, Field

from src.models import utility


class BaseOrjsonModel(BaseModel):
    """Base Model supporting orjson"""

    class Config:
        json_loads = orjson.loads
        json_dumps = utility.orjson_dumps


class UGCEvent(BaseOrjsonModel):
    dt: datetime = Field(default_factory=datetime.now)
