import datetime

from db.cache_factory import CacheAbstract
from settings.config import settings


class TokenService:

    def __init__(self, storage: CacheAbstract):
        self.storage = storage

    def set_revoked_access_token(self, user_id: str, revoked_access_token: str):
        _time = int(datetime.datetime.now().timestamp())
        self.storage.set(f'at_{user_id}_{_time}', revoked_access_token, settings.ACCESS_TOKEN_EXPIRE)

    def get_revoked_access_token(self, user_id: str) -> list[str]:
        keys = self.storage.keys(f'at_{user_id}*')
        values = [self.storage.get(key) for key in keys]
        return values

    def set_refresh_token(self, user_id: str, refresh_token: str) -> None:
        self.storage.set(f'rt_{user_id}', refresh_token, settings.REFRESH_TOKEN_EXPIRE)

    def get_refresh_token(self, user_id: str) -> str:
        return self.storage.get(f'rt_{user_id}')

    def delete_refresh_token(self, user_id: str) -> None:
        return self.storage.delete(f'rt_{user_id}')

    def delete_all_refresh_tokens(self):
        keys = self.storage.keys('rt_*')
        self.storage.delete(keys)

    def flushall(self) -> None:
        self.storage.flushall()
