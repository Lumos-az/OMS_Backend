from . import db
from sqlalchemy.sql import func


class PatientModel(db.Model):
    __tablename__ = 'Patient'
    pid = db.Column(db.VARCHAR(18),primary_key=True,nullable=False)
    name = db.Column(db.VARCHAR(100),nullable=False)
    age = db.Column(db.Integer,nullable=False)
    sex = db.Column(db.Text,nullable=False)
    phoneNumber = db.Column(db.Text,nullable=False)
    other = db.Column(db.Text)