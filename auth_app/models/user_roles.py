"""
This module stores the Role model.
"""

from db.db_factory import get_db
from models.base_model import BaseModel

db = get_db()


class Role(BaseModel):
    __tablename__ = 'role'
    __table_args__ = {'extend_existing': True}

    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.String(300))

    def __repr__(self):
        return '<Role %r>' % self.name

    @classmethod
    def find_by_id(cls, id: str):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
