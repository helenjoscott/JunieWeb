"""
Authentication forms for the Flask demo application.
"""

from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField,
    ValidationError
)
from wtforms.validators import (
    DataRequired, Length, Email, EqualTo
)

from ..models import User


class LoginForm(FlaskForm):
    """Form for user login."""
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=64)
    ])
    password = PasswordField('Password', validators=[
        DataRequired()
    ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    """Form for user registration."""
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=64)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(max=120)
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Register')

    def validate_username(self, field):
        """Check if username is already taken."""
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username is already taken.')

    def validate_email(self, field):
        """Check if email is already registered."""
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is already registered.')


class PasswordResetRequestForm(FlaskForm):
    """Form for requesting password reset."""
    email = StringField('Email', validators=[
        DataRequired(),
        Email(),
        Length(max=120)
    ])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, field):
        """Check if email exists."""
        user = User.query.filter_by(email=field.data).first()
        if user is None:
            raise ValidationError('Email address not found.')


class PasswordResetForm(FlaskForm):
    """Form for resetting password."""
    password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long')
    ])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Reset Password')