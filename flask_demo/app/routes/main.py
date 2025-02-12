"""
Main routes for the Flask demo application.
"""

from flask import Blueprint, render_template, current_app, request
from flask_login import login_required, current_user
from sqlalchemy import or_

from .. import db
from ..models import Item

# Create blueprint
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Home page route."""
    # Get latest items with pagination
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ITEMS_PER_PAGE']

    items = Item.query.order_by(Item.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template('main/index.html',
                         items=items,
                         title='Home')


@main_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard route."""
    # Get user's items with pagination
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ITEMS_PER_PAGE']

    user_items = current_user.items.order_by(Item.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)

    return render_template('main/dashboard.html',
                         items=user_items,
                         title='Dashboard')


@main_bp.route('/about')
def about():
    """About page route."""
    return render_template('main/about.html',
                         title='About')


@main_bp.route('/profile')
@login_required
def profile():
    """User profile route."""
    return render_template('main/profile.html',
                         title='Profile',
                         user=current_user)


@main_bp.route('/search')
def search():
    """Search route."""
    query = request.args.get('q', '')
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ITEMS_PER_PAGE']

    if query:
        # Search items by name or description
        items = Item.query.filter(
            db.or_(
                Item.name.ilike(f'%{query}%'),
                Item.description.ilike(f'%{query}%')
            )
        ).order_by(Item.created_at.desc())\
         .paginate(page=page, per_page=per_page, error_out=False)
    else:
        items = None

    return render_template('main/search.html',
                         items=items,
                         query=query,
                         title='Search')
