from pathlib import Path
from secrets import token_hex

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_user, logout_user
from PIL import Image

from app import app, bcrypt, db
from app.forms import (
    AccountUpdateForm,
    CreatePostForm,
    LoginForm,
    RegisterForm,
    UpdatePostForm,
)
from app.models import Post, User


@app.route("/")
def home():
    page = request.args.get("page", 1, type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=5)
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
        flash("You've Successfully Logged In!", "success")
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


# Save image in compressed form
def save_image(image):
    # Delete's the old Image (other than the 'default' Image)
    if current_user.picture != "default.jpg":
        old_path = Path.cwd() / "app" / "static" / "profile_pic" / current_user.picture
        old_path.unlink()

    name = token_hex(20)
    file_ext = Path(image.filename).suffix
    file_name = name + file_ext
    file_path = Path.cwd() / "app" / "static" / "profile_pic" / file_name
    output_size = (300, 300)
    img = Image.open(image)
    img.thumbnail(output_size)
    img.save(file_path)

    return file_name


@app.route("/account", methods=["POST", "GET"])
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


@app.route("/user/<string:username>")
def user(username):
    user = User.query.filter_by(username=username).first()
    page = request.args.get("page", 1, type=int)
    posts = (
        Post.query.filter_by(author=user)
        .order_by(Post.date.desc())
        .paginate(page=page, per_page=5)
    )
    return render_template("user.html", posts=posts, title=user.username, user=user)


@app.route("/post/<int:id>")
def post(id):
    post = Post.query.get(id)
    return render_template("post.html", post=post, title=post.title)


@app.route("/update-post/<int:id>", methods=["POST", "GET"])
def update_post(id):
    form = UpdatePostForm()
    post = Post.query.get(id)
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your Post has been Updated Successfully", "success")
        return redirect(url_for("home"))
    if request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", form=form, title="Update Post")


@app.route("/delete/post/<int:id>", methods=["POST", "GET"])
def delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    flash("Your Post has been Deleted Successfully!", "success")
    return redirect(url_for("home"))
