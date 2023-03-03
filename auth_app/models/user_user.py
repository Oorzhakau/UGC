"""
This module stores the User model.
"""
from sqlalchemy import or_
from sqlalchemy.dialects.postgresql import UUID
from werkzeug.security import generate_password_hash, check_password_hash

from db.db_factory import get_db
from models.base_model import BaseModel
from models.user_login_history import AccountHistory

db = get_db()

users_roles = db.Table(
    "users_roles",
    db.Column(
        "user_id",
        UUID(as_uuid=True),
        db.ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "role_id",
        UUID(as_uuid=True),
        db.ForeignKey("role.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    extend_existing=True,
)


class User(BaseModel):
    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}

    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String)
    email = db.Column(db.String(100), unique=True)
    roles = db.relationship(
        "models.user_roles.Role",
        secondary=users_roles,
        lazy=True,
        backref=db.backref("user", lazy="dynamic"),
    )
    history = db.relationship("AccountHistory", cascade="all, delete", backref="user")

    def __init__(self, username, password, id=None, email=None, name=None, roles=None):
        self.username = username
        self.password = generate_password_hash(password)
        self.name = name
        self.email = email
        if id:
            self.id = id
        if not roles:
            self.roles = []
        else:
            self.roles = roles

    def __repr__(self):
        return "<User %r>" % self.email

    def verify_password(self, pwd: str) -> bool:
        return check_password_hash(self.password, pwd)

    def is_admin(self):
        roles = [role.name for role in self.roles]
        if "admin" in roles:
            return True
        return False

    def change_password(self, pwd: str):
        self.password = generate_password_hash(pwd)
        super().save()

    @classmethod
    def find_by_username(cls, username: str):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_email(cls, email: str):
        return cls.query.filter_by(email=email).one_or_none()

    @classmethod
    def find_by_id(cls, id: str):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_user_by_universal_login(
        cls, username: str | None = None, email: str | None = None
    ):
        return cls.query.filter(
            or_(cls.username == username, cls.email == email)
        ).first()

    def add_history(self, user_agent: str, device: str, action: str = "signin"):
        row = AccountHistory(
            user=self, device=device, user_agent=user_agent, action=action
        )
        row.save()

    def get_history(self, limit=None):
        return (
            AccountHistory.query.filter_by(user=self)
            .order_by(AccountHistory.created_at.desc())
            .limit(limit)
            .all()
        )
