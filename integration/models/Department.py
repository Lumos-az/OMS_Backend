from . import db
from sqlalchemy.sql import func


class DepartmentModel(db.Model):
    __tablename__ = 'Department'
    Did = db.Column(db.BIGINT,primary_key=True,autoincrement=True,nullable=False)
    name = db.Column(db.Text)
    desp = db.Column(db.Text)
    cataloge = db.Column(db.Text)