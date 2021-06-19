from . import db


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
    sex = db.Column(db.Text)
    other = db.Column(db.Text)