from . import db
from sqlalchemy.sql import func


class ArticleSourceModel(db.Model):
    __tablename__ = 'article_source'
    Source_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Title = db.Column(db.String(32))
    Author = db.Column(db.String(32))
    Content = db.Column(db.String(500))
    Date = db.Column(db.DateTime, server_default = func.now())
    Type = db.Column(db.Integer)



