from . import db
from sqlalchemy.sql import func


class PresModel(db.Model):
    __tablename__ = 'pres'
    pres_id = db.Column(db.String(8), primary_key=True)
    user_id = db.Column(db.String(6))
    doctor_id = db.Column(db.String(6))
    information = db.Column(db.Text)
    time = db.Column(db.Text)
    prescription = db.Column(db.Text)
