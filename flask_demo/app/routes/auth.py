"""
Authentication routes for the Flask demo application.
"""

from flask import (
    Blueprint, render_template, redirect, url_for,
    flash, request, current_app
)
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse

from .. import db
from ..models import User
from ..forms.auth import LoginForm, RegistrationForm, PasswordResetRequestForm, PasswordResetForm

# Create blueprint
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """User registration route."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.password = form.password.data
        
        db.session.add(user)
        db.session.commit()
        
        flash('Congratulations, you are now a registered user!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html',
                         title='Register',
                         form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """User login route."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is None or not user.verify_password(form.password.data):
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        
        flash('You have been logged in successfully!', 'success')
        return redirect(next_page)
    
    return render_template('auth/login.html',
                         title='Login',
                         form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    """User logout route."""
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('main.index'))


@auth_bp.route('/reset-password-request', methods=['GET', 'POST'])
def reset_password_request():
    """Password reset request route."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            # Send password reset email
            send_password_reset_email(user)
        flash('Check your email for instructions to reset your password.', 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password_request.html',
                         title='Reset Password',
                         form=form)


@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Password reset route."""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    user = User.verify_reset_password_token(token)
    if not user:
        flash('Invalid or expired reset token.', 'error')
        return redirect(url_for('main.index'))
    
    form = PasswordResetForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash('Your password has been reset.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html',
                         title='Reset Password',
                         form=form)