import cloudinary
from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from app.config import Config

load_dotenv()


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()

login_manager.login_view = "users.login"
login_manager.login_message = "Please log in to view this page."
login_manager.login_message_category = "info"


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    cloudinary.config(
        cloud_name=app.config["CLOUD_NAME"],
        api_key=app.config["API_KEY"],
        api_secret=app.config["API_SECRET"],
        secure=True,
    )
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from app.errors.handlers import errors
    from app.main.routes import main
    from app.posts.routes import posts
    from app.users.routes import users

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
