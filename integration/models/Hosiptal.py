from . import db
from sqlalchemy.sql import func


class HospitalModel(db.Model):
    __tablename__ = 'Hospital'
    hid = db.Column(db.BIGINT,primary_key=True,autoincrement=True,nullable=False)
    name = db.Column(db.Text)
    pname = db.Column(db.Text)
    website = db.Column(db.Text)
    qualification = db.Column(db.Text)
    address = db.Column(db.Text)
    introduction = db.Column(db.Text)
    phone = db.Column(db.Text)
