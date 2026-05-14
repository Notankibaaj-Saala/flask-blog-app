from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.models import Post
from app.posts.forms import CreatePostForm, UpdatePostForm

posts = Blueprint("posts", __name__)


@posts.route("/create-post", methods=["POST", "GET"])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data, content=form.content.data, author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash("Your Post has been Created Successfully", "success")
        return redirect(url_for("main.home"))
    else:
        return render_template("create_post.html", form=form, title="Create Post")


@posts.route("/post/<int:id>")
def post(id):
    post = Post.query.get(id)
    return render_template("post.html", post=post, title=post.title)


@posts.route("/update/post/<int:id>", methods=["POST", "GET"])
@login_required
def update_post(id):
    post = Post.query.get(id)
    if current_user != post.author:
        abort(403)
    form = UpdatePostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your Post has been Updated Successfully", "success")
        return redirect(url_for("main.home"))
    if request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", form=form, title="Update Post")


@posts.route("/delete/post/<int:id>", methods=["POST", "GET"])
@login_required
def delete(id):
    post = Post.query.get(id)
    if current_user != post.author:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Your Post has been Deleted Successfully!", "success")
    return redirect(url_for("main.home"))
