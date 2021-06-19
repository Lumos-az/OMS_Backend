from . import db
from sqlalchemy.sql import func


class ReplyModel(db.Model):
    __tablename__ = 'reply'
    Reply_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Belong_Post_id = db.Column(db.Integer)
    Author_id = db.Column(db.String(32))
    Date = db.Column(db.DateTime, server_default=func.now())
    Content = db.Column(db.String(500))
    file = db.Column(db.String(255))


class ReplyReportModel(db.Model):
    __tablename__ = 'reply_report'
    report_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reply_id = db.Column(db.Integer)
    reporter_id = db.Column(db.String(33))
    content = db.Column(db.String(255))