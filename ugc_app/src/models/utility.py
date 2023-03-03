"""
Utility functions storage
"""
import orjson


def orjson_dumps(v, *, default):
    """
    As orjson.dumps returns bytes, while pydantic
    demand unicode, we need to decode the bytes.
    """
    return orjson.dumps(v, default=default).decode()
