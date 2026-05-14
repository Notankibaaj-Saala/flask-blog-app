from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import bcrypt, db
from app.models import Post, User
from app.users.forms import (
    AccountUpdateForm,
    ForgotPassword,
    LoginForm,
    RegisterForm,
    ResestPasswordForm,
)
from app.users.utils import save_image, send_mail

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash(
            "You're already logged In. Logout first, in order to Register again!",
            "info",
        )
        return redirect(url_for("main.home"))
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
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form, title="Register Form")


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash(
            "You're already logged In. Logout first, in order to Login again!",
            "info",
        )
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=form.remember.data)
        flash("You've Successfully Logged In!", "success")
        nxt = request.args.get("next")
        print(nxt)
        return redirect(nxt) if nxt else redirect(url_for("main.home"))
    else:
        return render_template("login.html", form=form, title="Login Form")


@users.route("/logout")
def logout():
    if not current_user.is_authenticated:
        flash("Login first in order to Logout", "info")
    else:
        logout_user()
    return redirect(url_for("main.home"))


@users.route("/account", methods=["POST", "GET"])
@login_required
def account():
    form = AccountUpdateForm()
    if form.validate_on_submit():
        if form.image.data:
            image = save_image(form.image.data)
            current_user.picture = image
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your Account has been Updated!", "success")
        return redirect("/account")
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image = url_for("static", filename="profile_pic/" + current_user.picture)
    return render_template(
        "account.html", form=form, image=image, title="Update Account"
    )


@users.route("/user/<string:username>")
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get("page", 1, type=int)
    posts = (
        Post.query.filter_by(author=user)
        .order_by(Post.date.desc())
        .paginate(page=page, per_page=5)
    )
    return render_template("user.html", posts=posts, title=username, user=user)


@users.route("/reset-password", methods=["POST", "GET"])
def reset_request():
    form = ForgotPassword()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        token = user.token_generator()
        send_mail(user, token)
        flash("An Email has been sent with the Details to Reset your Password", "info")
        return redirect(url_for("main.home"))
    else:
        return render_template(
            "reset_request.html", form=form, title="Password Reset Form"
        )


@users.route("/reset-password/<token>", methods=["POST", "GET"])
def reset_password(token):
    user = User.token_verification(token)
    if user == "Expired":
        return redirect(url_for("users.reset_request"))
    elif user == "Modified":
        return redirect(url_for("main.home"))
    form = ResestPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password1.data).decode()
        user.password = hashed_password
        db.session.commit()
        flash("Your Password has been changed Successfully", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_password.html", form=form, title="Reset Password")
