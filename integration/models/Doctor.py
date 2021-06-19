from . import db
from sqlalchemy.sql import func


class DoctorModel(db.Model):
    __tablename__ = 'Doctor'
    did = db.Column(db.BIGINT,primary_key=True,autoincrement=True,nullable=False)
    name = db.Column(db.VARCHAR(255),nullable=False)
    phone = db.Column(db.VARCHAR(255),nullable=False)
    mail = db.Column(db.VARCHAR(255))
    avatarUrl = db.Column(db.VARCHAR(255))
    profession = db.Column(db.VARCHAR(255))
    introduction = db.Column(db.Text)
    skilledField = db.Column(db.Text)
    hid = db.Column(db.BIGINT)
    Depid = db.Column(db.BIGINT)