from . import db
from sqlalchemy.sql import func


class PostModel(db.Model):
    __tablename__ = 'post'
    Post_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Author_id = db.Column(db.String(32))
    Date = db.Column(db.DateTime, server_default=func.now())
    Title = db.Column(db.String(50))
    Content = db.Column(db.String(500))
    Type = db.Column(db.Integer)