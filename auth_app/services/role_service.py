from functools import lru_cache

from sqlalchemy.exc import DataError

from db.db_factory import get_db, SQLAlchemy
from models import Role
from schemas import RoleScheme


class RoleService:

    def __init__(self, db_storage: SQLAlchemy):
        self.client = db_storage

    def get_roles(self):
        return Role.query.all()

    def get_or_create_role(self, name: str, description: str | None) -> Role:
        role = Role.query.filter_by(name=name).first()
        if role:
            return role
        else:
            role = Role(name=name, description=description)
            role.save()
            return role

    def get_by_id(self, id: str) -> Role | None:
        try:
            return Role.find_by_id(id)
        except DataError:
            return

    def get_by_name(self, name: str) -> Role:
        return Role.find_by_name(name)

    @staticmethod
    def change_role_data(role_id: str, role_patch: RoleScheme) -> Role | None:
        role = Role.find_by_id(role_id)
        if role:
            body = role_patch.dict(exclude={'id'})
            for field in body:
                setattr(role, field, body[field])
            role.save()
            return Role.find_by_id(role_id)
        return None


@lru_cache()
def get_role_service() -> RoleService:
    db_storage = get_db()
    return RoleService(db_storage)
