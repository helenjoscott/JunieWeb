"""
Email utilities for the Flask demo application.
"""

from threading import Thread
from flask import current_app, render_template
from flask_mail import Message

from .. import mail


def send_async_email(app, msg):
    """Send email asynchronously."""
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, text_body, html_body, sender=None):
    """Send email with both text and HTML versions."""
    if sender is None:
        sender = current_app.config['MAIL_DEFAULT_SENDER']
    
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    
    # Send email in a background thread
    Thread(
        target=send_async_email,
        args=(current_app._get_current_object(), msg)
    ).start()


def send_password_reset_email(user):
    """Send password reset email to user."""
    token = user.get_reset_password_token()
    send_email(
        subject='Reset Your Password',
        recipients=[user.email],
        text_body=render_template('email/reset_password.txt',
                                user=user, token=token),
        html_body=render_template('email/reset_password.html',
                                user=user, token=token)
    )


def send_confirmation_email(user):
    """Send email confirmation to user."""
    token = user.get_confirmation_token()
    send_email(
        subject='Confirm Your Email',
        recipients=[user.email],
        text_body=render_template('email/confirm_email.txt',
                                user=user, token=token),
        html_body=render_template('email/confirm_email.html',
                                user=user, token=token)
    )