"""
RESTful API routes for the Flask demo application.
"""

from flask import Blueprint, jsonify, request, url_for, current_app
from flask_login import current_user, login_required
from werkzeug.exceptions import BadRequest, NotFound, Forbidden

from .. import db
from ..models import Item, User

# Create blueprint
api_bp = Blueprint('api', __name__)


def validate_item_data(data):
    """Validate item data from request."""
    if not data:
        raise BadRequest("No data provided")
    
    required_fields = ['name', 'price']
    for field in required_fields:
        if field not in data:
            raise BadRequest(f"Missing required field: {field}")
    
    if not isinstance(data['name'], str) or len(data['name']) < 1:
        raise BadRequest("Name must be a non-empty string")
    
    if not isinstance(data['price'], (int, float)) or data['price'] < 0:
        raise BadRequest("Price must be a non-negative number")
    
    return data


@api_bp.route('/items', methods=['GET'])
def get_items():
    """Get list of items with pagination."""
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ITEMS_PER_PAGE']
    
    items = Item.query.order_by(Item.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [item.to_dict() for item in items.items],
        'total': items.total,
        'page': items.page,
        'per_page': items.per_page,
        'pages': items.pages,
        '_links': {
            'self': url_for('api.get_items', page=page, _external=True),
            'next': url_for('api.get_items', page=page + 1, _external=True)
                   if items.has_next else None,
            'prev': url_for('api.get_items', page=page - 1, _external=True)
                   if items.has_prev else None
        }
    })


@api_bp.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    """Get a specific item."""
    item = Item.query.get_or_404(id)
    return jsonify(item.to_dict())


@api_bp.route('/items', methods=['POST'])
@login_required
def create_item():
    """Create a new item."""
    data = request.get_json() or {}
    data = validate_item_data(data)
    
    item = Item(
        name=data['name'],
        description=data.get('description', ''),
        price=data['price'],
        owner=current_user
    )
    
    db.session.add(item)
    db.session.commit()
    
    response = jsonify(item.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_item', id=item.id)
    return response


@api_bp.route('/items/<int:id>', methods=['PUT'])
@login_required
def update_item(id):
    """Update an existing item."""
    item = Item.query.get_or_404(id)
    
    if item.owner != current_user:
        raise Forbidden("You don't have permission to modify this item")
    
    data = request.get_json() or {}
    data = validate_item_data(data)
    
    item.name = data['name']
    item.description = data.get('description', item.description)
    item.price = data['price']
    
    db.session.commit()
    return jsonify(item.to_dict())


@api_bp.route('/items/<int:id>', methods=['DELETE'])
@login_required
def delete_item(id):
    """Delete an item."""
    item = Item.query.get_or_404(id)
    
    if item.owner != current_user:
        raise Forbidden("You don't have permission to delete this item")
    
    db.session.delete(item)
    db.session.commit()
    return '', 204


@api_bp.route('/users/<int:id>/items', methods=['GET'])
def get_user_items(id):
    """Get items for a specific user."""
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ITEMS_PER_PAGE']
    
    items = user.items.order_by(Item.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'items': [item.to_dict() for item in items.items],
        'total': items.total,
        'page': items.page,
        'per_page': items.per_page,
        'pages': items.pages,
        '_links': {
            'self': url_for('api.get_user_items', id=id, page=page, _external=True),
            'next': url_for('api.get_user_items', id=id, page=page + 1, _external=True)
                   if items.has_next else None,
            'prev': url_for('api.get_user_items', id=id, page=page - 1, _external=True)
                   if items.has_prev else None,
            'user': url_for('api.get_user', id=id, _external=True)
        }
    })


@api_bp.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    """Get user information."""
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())