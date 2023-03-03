from redis import Redis


def get_revoked_access_tokens(user_id: str, redis: Redis) -> list[str]:
    revoked_keys = redis.keys(f"at_{user_id}*")
    revoked_values = [redis.get(key) for key in revoked_keys]
    return revoked_values
