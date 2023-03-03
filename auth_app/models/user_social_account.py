from sqlalchemy.dialects.postgresql import UUID

from db.db_factory import get_db
from models.base_model import BaseModel
from models.user_user import User

db = get_db()


class SocialAccount(BaseModel):
    __tablename__ = "social_account"

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("user.id"), nullable=False)
    user = db.relationship(User, backref=db.backref("social_accounts", lazy=True))

    social_id = db.Column(db.Text, nullable=False)
    social_name = db.Column(db.Text, nullable=False)

    __table_args__ = (
        db.UniqueConstraint("social_id", "social_name", name="social_pk"),
    )

    def __repr__(self):
        return f"<SocialAccount {self.social_name}:{self.user_id}>"
