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
    file = db.Column(db.String(255))


class PostReportModel(db.Model):
    __tablename__ = 'post_report'
    report_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer)
    reporter_id = db.Column(db.String(33))
    content = db.Column(db.String(255))
