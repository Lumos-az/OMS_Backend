from . import db
from sqlalchemy.sql import func


class ReplyModel(db.Model):
    __tablename__ = 'reply'
    Reply_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Belong_Post_id = db.Column(db.Integer)
    Author_id = db.Column(db.String(32))
    Date = db.Column(db.DateTime, server_default = func.now())
    Content = db.Column(db.String(500))
