from . import db


class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(32), primary_key=True)
    password = db.Column(db.String(32))
    identity = db.Column(db.Integer)
    Can_post = db.Column(db.Integer)
    Can_reply = db.Column(db.Integer)