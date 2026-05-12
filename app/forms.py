from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    EmailField,
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.models import Post, User


class RegisterForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password1 = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password1")]
    )
    submit = SubmitField("Register")

    # usrnm = self.username (form.username)
    def validate_username(self, usrnm):
        if User.query.filter_by(username=usrnm.data).first():
            raise ValidationError("Username already taken. Choose something else!")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("Email already exists. Choose something else!")


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

    def validate_username(self, usrnm):
        if not User.query.filter_by(username=usrnm.data).first():
            raise ValidationError("No User found for this Username!")


class CreatePostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Create Post")

    def validate_content(self, content):
        if Post.query.filter_by(content=content.data).first():
            raise ValidationError("Post Already Exists. Write Something else!")
