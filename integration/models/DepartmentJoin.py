from . import db
from sqlalchemy.sql import func


class DepartmentJoinModel(db.Model):
    __tablename__ = 'DepartmentJoin'
    did = db.Column(db.BIGINT,primary_key=True,nullable=False)
    hid = db.Column(db.BIGINT,primary_key=True,nullable=False)