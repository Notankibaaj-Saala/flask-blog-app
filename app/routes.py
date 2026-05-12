from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from app import app, bcrypt, db
from app.forms import LoginForm, RegisterForm
from app.models import User

posts = [
    {
        "title": "AOT",
        "content": "Attack On Titan",
        "date": "Apr 7 2013",
        "author": "Hajime Isayama",
    },
    {
        "title": "TQQ",
        "content": "The Quintessential Quintuplets",
        "date": "May 5 2005",
        "author": "Negi Haruba",
    },
]


@app.route("/")
def home():

    return render_template("home.html", posts=posts, title="Blog Home")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        password = form.password1.data
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        flash("Your Account has been Created Successfully!", "success")
        return redirect(url_for("login"))
    else:
        return render_template("register.html", form=form, title="Register Form")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username="form.username.data").first()
        login_user(user, remember=form.remember.data)
        flash("Account Created Successfully! You can now Log In.", "success")
        return redirect(url_for("home"))
    else:
        return render_template("login.html", form=form, title="Login Form")


@app.route("/logout")
def logout():
    if not current_user.is_authenticated:
        flash("Login first in order to Logout", "info")
    else:
        logout_user()
    return redirect(url_for("home"))
