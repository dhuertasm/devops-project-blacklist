import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Usuarios(db.Model):

    __tablename__ = 'usuarios'
    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username: str = db.Column(db.String(150))
    email: str = db.Column(db.String(150))
    password: str = db.Column(db.Text)
    salt: str = db.Column(db.String(150))
    token: str = db.Column(db.String(500), nullable=True)
    expireAt: datetime = db.Column(db.DateTime, default=datetime.datetime.now)
    createdAt: datetime = db.Column(db.DateTime, default=datetime.datetime.now)
