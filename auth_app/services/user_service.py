from functools import lru_cache

from device_detector import DeviceDetector
from sqlalchemy.exc import DataError
from flask_jwt_extended import create_access_token, create_refresh_token

from db.cache_factory import CacheAbstract, get_redis_extended
from db.db_factory import get_db
from models import User, Role, AccountHistory, SocialAccount
from enumeration import RolesEnum
from services.token_service import TokenService
from services.utils import generate_random_string
from schemas.schemas import TokensResponse, AccountScheme, RolesRequest


class UserService:

    def __init__(self, cache_storage: CacheAbstract):
        self.token_service = TokenService(cache_storage)
        self.db = get_db()

    def create_tokens(self, user: User) -> TokensResponse:
        token_user_header = {'user_id': user.id}
        token_user_claim = token_user_header.copy()
        token_user_claim['roles'] = [role.name for role in user.roles]
        token_user_claim['username'] = user.username

        access_token = create_access_token(identity=token_user_header, additional_claims=token_user_claim)
        refresh_token = create_refresh_token(identity=token_user_header, additional_claims=token_user_claim)
        self.token_service.set_refresh_token(user.id, refresh_token)
        response = TokensResponse(access_token=access_token, refresh_token=refresh_token)
        return response

    def revoke_access_token(self, user_id: str, revoked_access_token: str) -> None:
        self.token_service.set_revoked_access_token(user_id, revoked_access_token)

    def logout_user(self, user_id: str, access_token: str) -> None:
        self.token_service.set_revoked_access_token(user_id, access_token)
        self.token_service.delete_refresh_token(user_id)

    def logout_all_user(self) -> None:
        self.token_service.delete_all_refresh_tokens()

    def check_access_token_is_revoked(self, user_id: str, access_token: str) -> bool:
        revokes_access_tokens = self.token_service.get_revoked_access_token(user_id)
        return access_token in revokes_access_tokens

    def check_refresh_token(self, user_id: str, refresh_token: str) -> bool:
        return refresh_token == self.token_service.get_refresh_token(user_id)

    @staticmethod
    def add_action_in_history(user: User, user_agent: str, action: str = 'signin') -> None:
        device = DeviceDetector(user_agent).parse()
        device_type = (device.device_type()
                       if device.device_type() in ["desktop", "smartphone", "tv"]
                       else "unknown")
        history = AccountHistory(
            user_id=user.id,
            user_agent=device.client_name(),
            device=device_type,
            action=action
        )
        history.save()

    @staticmethod
    def get_account_history(user: User, page: int = 1, per_page: int = 1):
        return AccountHistory.query.filter_by(user_id=user.id).paginate(page=page, per_page=per_page)

    @staticmethod
    def create_user(username: str, password: str, roles_name: list[str] | None, **kwargs) -> None:
        if not roles_name:
            roles_name = list(RolesEnum.BASE)
        roles = []
        for role_name in roles_name:
            role = Role.find_by_name(name=role_name)
            if not role:
                role = Role(name=role_name)
                role.save()
            roles.append(role)
        user = User(username=username, password=password, **kwargs)
        user.roles = roles
        user.save()

    @staticmethod
    def create_superuser(username: str, password: str, **kwargs) -> None:
        role = Role.find_by_name(name=RolesEnum.ADMIN)
        if not role:
            role = Role(name=RolesEnum.ADMIN)
            role.save()
        user = User(username=username, password=password, roles=[role], **kwargs)
        user.save()

    def create_oauth_user(self,
                          social_id: str,
                          social_name: str,
                          email: str | None = None,
                          username: str | None = None) -> SocialAccount:
        user = User.get_user_by_universal_login(email=email, username=username)
        if not user:
            role = Role.get_or_create(name=RolesEnum.BASE)
            if not username and email:
                username = email.split('@')[0]
            password = generate_random_string()
            user = User(
                username=username,
                password=password,
                email=email,
                roles=[role],
            )
            user.save()
        account = SocialAccount(social_id=social_id, social_name=social_name, user=user)
        self.db.session.add(account)
        self.db.session.commit()
        return account

    @staticmethod
    def change_password(user: User, password: str):
        user.change_password(password)

    @staticmethod
    def change_user_data(user_patch: AccountScheme) -> None:
        user = User.find_by_username(user_patch.username)
        if user:
            body = user_patch.dict(exclude={'username'})
            for field in body:
                setattr(user, field, body[field])
            user.save()

    @staticmethod
    def get_users(page: int = 1, per_page: int = 1):
        return User.query.paginate(page=page, per_page=per_page)

    @staticmethod
    def get_user_by_username(username: str) -> User:
        return User.find_by_username(username=username)

    @staticmethod
    def get_user_by_id(user_id: str) -> User | None:
        try:
            return User.find_by_id(user_id)
        except DataError:
            return None

    @staticmethod
    def get_social_account(social_id: str, social_name: str) -> SocialAccount:
        return SocialAccount.query.filter_by(social_id=social_id, social_name=social_name).one_or_none()

    @staticmethod
    def add_roles_for_user(user: User, roles: list[Role]) -> None:
        for role in roles:
            user.roles.add(role)
        user.save()

    def remove_roles_from_user(self, user_id: str, roles_new: RolesRequest) -> User:
        user = self.get_user_by_id(user_id)
        for name in roles_new.roles:
            role = Role.find_by_name(name)
            try:
                user.roles.remove(role)
            except ValueError:
                continue
        user.save()
        return self.get_user_by_id(user_id)

    def change_roles_from_user(self, user_id: str, roles_new: RolesRequest) -> User:
        user = self.get_user_by_id(user_id)
        temp = []
        for name in roles_new.roles:
            role = Role.find_by_name(name)
            if role:
                temp.append(role)
        user.roles = temp
        user.save()
        return self.get_user_by_id(user_id)


@lru_cache()
def get_user_service() -> UserService:
    cache_storage = get_redis_extended()
    return UserService(cache_storage)
