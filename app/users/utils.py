from cloudinary.uploader import upload
from flask import url_for
from flask_mail import Message

from app import mail


def save_image(image):

    result = upload(image)

    return result["secure_url"]


def send_mail(user, token):
    print(user.email)
    msg = Message("Password Reset", recipients=[user.email], sender="noreply@demo.com")
    msg.body = f"""To Reset Your Password, visit the following link:
  {url_for("users.reset_password", token=token, _external=True)}
If you did not make this request. Simply ignore this request and no changes will be made.
"""
    mail.send(msg)
