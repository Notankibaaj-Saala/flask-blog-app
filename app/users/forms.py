from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.models import User


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


class AccountUpdateForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = EmailField("Email", validators=[DataRequired(), Email()])
    image = FileField("Choose Image", validators=[FileAllowed(["png", "jpg"])])
    submit = SubmitField("Update Profile")

    def validate_username(self, usrnm):
        if current_user.username != usrnm.data:
            if User.query.filter_by(username=usrnm.data).first():
                raise ValidationError("Username already taken. Choose something else!")

    def validate_email(self, email):
        if current_user.email != email.data:
            if User.query.filter_by(email=email.data).first():
                raise ValidationError("Email already exists. Choose something else!")


class ForgotPassword(FlaskForm):
    email = EmailField("Email", validators=[Email()])
    submit = SubmitField("Send Email")

    def validate_email(self, email):
        if not User.query.filter_by(email=email.data).first():
            raise ValidationError("No User with that Email")


class ResestPasswordForm(FlaskForm):
    password1 = PasswordField("New Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password1")]
    )
    submit = SubmitField("Reset Password")
