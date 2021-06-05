from . import db
from sqlalchemy.sql import func

class UserModel(db.Model):
    __tablename__ = 'userinfo'
    uid = db.Column(db.String(33), primary_key=True)
    password = db.Column(db.String(50))
    nickname = db.Column(db.String(50))
    name = db.Column(db.String(50))
    address = db.Column(db.String(50))
    phoneNumber = db.Column(db.String(20))
    emailAddr = db.Column(db.String(30))
    utype = db.Column(db.Integer)
    age = db.Column(db.Integer)
    sex = db.Column(db.String(10))
    other = db.Column(db.String(150))

class DocModel(db.Model):
    __tablename__ = 'DoctorPart1'
    did = db.Column(db.String(33), primary_key=True)
    profield = db.Column(db.String(255))
    hospital = db.Column(db.String(100))
    room = db.Column(db.String(100))
    introduction = db.Column(db.String(500))
    activated = db.Column(db.Integer)