import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class BlackList(db.Model):

    __tablename__ = 'blacklist'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email: str = db.Column(db.String(150))
    app_uuid: str = db.Column(db.String(250))
    blocked_reason: str = db.Column(db.String(255))
    token: str = db.Column(db.String(500), nullable=True)
    ip: str = db.Column(db.String(150))
    createdAt: datetime = db.Column(db.DateTime, default=datetime.datetime.now)
