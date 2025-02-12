"""
Error handlers for the Flask demo application.
"""

from flask import render_template, request, jsonify
from werkzeug.exceptions import HTTPException


def is_api_request():
    """Check if the request is for the API."""
    return request.path.startswith('/api/')


def handle_400_error(e):
    """Handle 400 Bad Request error."""
    if is_api_request():
        return jsonify({
            'error': 'Bad Request',
            'message': str(e),
            'status_code': 400
        }), 400
    return render_template('errors/400.html', error=e), 400


def handle_401_error(e):
    """Handle 401 Unauthorized error."""
    if is_api_request():
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Authentication required',
            'status_code': 401
        }), 401
    return render_template('errors/401.html'), 401


def handle_403_error(e):
    """Handle 403 Forbidden error."""
    if is_api_request():
        return jsonify({
            'error': 'Forbidden',
            'message': str(e),
            'status_code': 403
        }), 403
    return render_template('errors/403.html', error=e), 403


def handle_404_error(e):
    """Handle 404 Not Found error."""
    if is_api_request():
        return jsonify({
            'error': 'Not Found',
            'message': 'The requested resource was not found',
            'status_code': 404
        }), 404
    return render_template('errors/404.html'), 404


def handle_405_error(e):
    """Handle 405 Method Not Allowed error."""
    if is_api_request():
        return jsonify({
            'error': 'Method Not Allowed',
            'message': 'The method is not allowed for the requested URL',
            'status_code': 405
        }), 405
    return render_template('errors/405.html'), 405


def handle_429_error(e):
    """Handle 429 Too Many Requests error."""
    if is_api_request():
        return jsonify({
            'error': 'Too Many Requests',
            'message': 'Rate limit exceeded',
            'status_code': 429
        }), 429
    return render_template('errors/429.html'), 429


def handle_500_error(e):
    """Handle 500 Internal Server Error."""
    if is_api_request():
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'An internal server error occurred',
            'status_code': 500
        }), 500
    return render_template('errors/500.html'), 500


def handle_generic_error(e):
    """Handle any other HTTP exception."""
    if isinstance(e, HTTPException):
        if is_api_request():
            return jsonify({
                'error': e.name,
                'message': e.description,
                'status_code': e.code
            }), e.code
        return render_template('errors/generic.html', error=e), e.code
    
    # Handle non-HTTP exceptions
    if is_api_request():
        return jsonify({
            'error': 'Internal Server Error',
            'message': str(e),
            'status_code': 500
        }), 500
    return render_template('errors/500.html', error=e), 500


def register_error_handlers(app):
    """Register error handlers with the Flask application."""
    app.register_error_handler(400, handle_400_error)
    app.register_error_handler(401, handle_401_error)
    app.register_error_handler(403, handle_403_error)
    app.register_error_handler(404, handle_404_error)
    app.register_error_handler(405, handle_405_error)
    app.register_error_handler(429, handle_429_error)
    app.register_error_handler(500, handle_500_error)
    app.register_error_handler(Exception, handle_generic_error)