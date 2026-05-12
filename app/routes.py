from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_user, logout_user

from app import app, bcrypt, db
from app.forms import CreatePostForm, LoginForm, RegisterForm
from app.models import Post, User


@app.route("/")
def home():
    db.create_all()
    posts = Post.query.all()
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
    return render_template("register.html", form=form, title="Register Form")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
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


@app.route("/create-post", methods=["POST", "GET"])
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data, content=form.content.data, author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash("Your Post has been Created Successfully", "success")
        return redirect(url_for("home"))
    else:
        return render_template("create_post.html", form=form, title="Create Post")
