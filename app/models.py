from datetime import datetime

from flask_login import UserMixin

from app import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    picture = db.Column(db.String(80), default="default.jpg")
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return self.username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeginKey("user.id"), nullable=False)

    def __repr__(self):
        return self.title
