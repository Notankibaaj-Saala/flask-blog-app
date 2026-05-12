from flask import render_template

from app import app

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
