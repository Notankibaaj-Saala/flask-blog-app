from pathlib import Path
from secrets import token_hex

from flask import url_for
from flask_login import current_user
from flask_mail import Message
from PIL import Image

from app import mail


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


def send_mail(user, token):
    print(user.email)
    msg = Message("Password Reset", recipients=[user.email], sender="noreply@demo.com")
    msg.body = f"""To Reset Your Password, visit the following link:
  {url_for("users.reset_password", token=token, _external=True)}
If you did not make this request. Simply ignore this request and no changes will be made.
"""
    mail.send(msg)
