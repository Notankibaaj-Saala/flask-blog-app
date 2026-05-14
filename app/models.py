from datetime import datetime

from flask import current_app, flash
from flask_login import UserMixin
from itsdangerous import BadSignature, SignatureExpired
from itsdangerous import URLSafeTimedSerializer as Serializer

from app import db, login_manager


@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    picture = db.Column(db.Text, nullable=False, default="https://res.cloudinary.com/dnp9m5bqj/image/upload/v1778784325/default_jazgao.jpg")
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return self.username

    def token_generator(self):
        s = Serializer(current_app.secret_key)
        return s.dumps(self.id, salt="Helu")

    @staticmethod
    def token_verification(token):
        s = Serializer(current_app.secret_key)
        try:
            uid = s.loads(token, salt="Helu", max_age=1800)
        except SignatureExpired:
            flash("Your link has expired. Please request a new one.", "warning")
            return "Expired"
        except BadSignature:
            flash("Invalid or Tampered link.", "danger")
            return "Modified"
        else:
            return User.query.get(uid)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return self.title
