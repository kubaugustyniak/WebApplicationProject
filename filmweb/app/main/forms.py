from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, InputRequired, EqualTo

class CommentForm(FlaskForm):
    body=TextAreaField("Comment", validators=[DataRequired()])
    submit = SubmitField('Submit')