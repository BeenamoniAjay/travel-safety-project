from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
from ..models import User


class SignupForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(message='Please enter an email.'), Email(message='Please enter a valid email address.')]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(message='Please enter a password.'), Length(min=6)]
    )
    confirm_password = PasswordField(
        'Confirm password',
        validators=[DataRequired(message='Please confirm your password.'), EqualTo('password', message='Passwords must match.')]
    )
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        if User.query.filter_by(email=email.data.strip().lower()).first():
            raise ValidationError('This email is already registered.')


class LoginForm(FlaskForm):
    email = StringField(
        'Email',
        validators=[DataRequired(message='Please enter your email.'), Email(message='Please enter a valid email address.')]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired(message='Please enter your password.')]
    )
    submit = SubmitField('Log In')
