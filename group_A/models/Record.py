from . import db
from sqlalchemy.sql import func


class RecordModel(db.Model):
    __tablename__ = 'Record'
    rid = db.Column(db.BIGINT,primary_key=True,nullable=False,autoincrement=True)
    name = db.Column(db.VARCHAR(100),nullable=False)
    reservationNumber = db.Column(db.Integer,nullable=False)
    identityNumber = db.Column(db.VARCHAR(18),nullable=False)
    phoneNumber = db.Column(db.Text,nullable=False)
    hospitalid = db.Column(db.BIGINT,nullable=False)
    timeid = db.Column(db.Integer,nullable=False)
    doctorid = db.Column(db.BIGINT,nullable=False)
    departmentid = db.Column(db.BIGINT,nullable=False)
    others = db.Column(db.Text)

