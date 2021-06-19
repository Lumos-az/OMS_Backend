from . import db
from sqlalchemy.sql import func


class BookingTimeModel(db.Model):
    __tablename__ = 'BookingTime'
    tid = db.Column(db.Integer, primary_key=True, nullable=False,autoincrement=True)
    date = db.Column(db.Date,primary_key=True,nullable=False)
    time = db.Column(db.Text,nullable=False)
    isFull = db.Column(db.SMALLINT,nullable=False)
    state = db.Column(db.SMALLINT,nullable=False)
    did = db.Column(db.BIGINT,primary_key=True,nullable=False)