import datetime
import uuid

from sqlalchemy.dialects.postgresql import UUID

from db.db_factory import get_db

db = get_db()


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    modified = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow,
                         onupdate=datetime.datetime.utcnow)

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_or_create(cls, **kwargs):
        instance = cls.query.filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = cls(**kwargs)
            db.session.add(instance)
            db.session.commit()
            return instance
