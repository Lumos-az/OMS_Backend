from . import db
from sqlalchemy.sql import func


class PatientsJoinModel(db.Model):
    __tablename__ = 'PatientsJoin'
    uid = db.Column(db.VARCHAR(18),primary_key=True,nullable=False)
    pid = db.Column(db.VARCHAR(18),primary_key=True,nullable=False)
    isDefault = db.Column(db.Integer,nullable=False)