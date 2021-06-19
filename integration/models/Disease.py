from . import db
from sqlalchemy.sql import func


class DiseaseModel(db.Model):
    __tablename__ = 'Disease'
    iid = db.Column(db.BIGINT,primary_key=True,nullable=False,autoincrement=True)
    Did = db.Column(db.BIGINT,nullable=False)
    iname = db.Column(db.VARCHAR(255),nullable=False)
    desp = db.Column(db.Text)
    reason = db.Column(db.Text)
    symptom = db.Column(db.Text)
    treatment = db.Column(db.Text)