from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError

from app.models import Post


class CreatePostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Create Post")

    def validate_content(self, content):
        if Post.query.filter_by(content=content.data).first():
            raise ValidationError("Post Already Exists. Write Something else!")


class UpdatePostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Update Post")

    def validate_content(self, content):
        if Post.query.filter_by(content=content.data).first():
            raise ValidationError("Post Already Exists. Write Something else!")
