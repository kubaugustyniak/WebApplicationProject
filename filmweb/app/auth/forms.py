from ..models import User
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, InputRequired, EqualTo
from wtforms import ValidationError



class LoginForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired(), Length(1,64)])
    password=PasswordField('Password', validators=[DataRequired()])
    submit=SubmitField('Log In')

class RegistrationForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(),Length(1,64),Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64),
        Regexp('[A-Za-z][A-Za-z0-9_.]*$', 0, 'Usernames must have only letters, numbers,'
                                                          ' dots or'
                                                          ' underscores')
    ])
    first_name = StringField('First name', validators=[DataRequired(), Length(1, 64)])
    last_name = StringField('Last name', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Password must match.')
    ])
    password2 = PasswordField('Confirm password', validators=[
        DataRequired()
    ])
    submit = SubmitField('Register')

    def validate_email(self, field):  # checking email exsisting in database
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):  # checking username existing in database
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already in use')

#Form for change_password.html
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[
        DataRequired(), EqualTo('password2', message='Password must match')
    ])
    password2 = PasswordField('Confirm new password',
                              validators=[DataRequired()])
    submit = SubmitField('Update Password')
#Forms to reset password
class PasswordResetRequestForm(FlaskForm):      #first form -> you give an email
    email = StringField('Email', validators=[
        DataRequired(), Length(1,64), Email()
    ])
    submit = SubmitField('Reset Password')

class PasswordResetForm(FlaskForm):     #second form -> you give new password and confirm it
    password = PasswordField('New Password', validators=[
        DataRequired(), EqualTo('password2', message='Password must match')

    ])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit= SubmitField('Reset Password')

#Form for change_email.html
class ChangeEmailForm(FlaskForm):
    email =StringField('New Email', validators=[
        DataRequired(), Length(1,64), Email()
    ])
    password = PasswordField('Password', validators=[DataRequired()])
    submit= SubmitField('Update Email Address')

    def validate_email(self,field):     #checking email existing in database
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')