"""
This module stores the account history model.
"""
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from db.db_factory import get_db
from models.base_model import BaseModel

db = get_db()


def create_partition(target, connection, **kw) -> None:
    """ creating partition by user_sign_in """
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "history_smart" PARTITION OF "history" FOR VALUES IN ('smartphone')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "history_mobile" PARTITION OF "history" FOR VALUES IN ('desktop')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "history_web" PARTITION OF "history" FOR VALUES IN ('tv')"""
    )
    connection.execute(
        """CREATE TABLE IF NOT EXISTS "history_unknown" PARTITION OF "history" FOR VALUES IN ('unknown')"""
    )


class AccountHistory(BaseModel):
    __tablename__ = "history"
    __table_args__ = (
        UniqueConstraint('id', 'device'),
        {
            'postgresql_partition_by': 'LIST (device)',
            'listeners': [('after_create', create_partition)],
        }
    )

    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    user_agent = db.Column(db.String, nullable=False)
    device = db.Column(db.String, primary_key=True)
    action = db.Column(db.String, default="signin")

    def __repr__(self):
        return "<AuthHistory %r>" % self.id
