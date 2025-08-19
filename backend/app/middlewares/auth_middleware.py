from functools import wraps
from flask import request, jsonify

from app.services.auth_service import AuthService


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({
                'error': 'Authentication token is missing',
                'message': 'Please provide a valid authentication token in the Authorization header'
            }), 401
        
        current_user = AuthService.verify_token(token)
        
        if not current_user:
            return jsonify({
                'error': 'Invalid authentication token',
                'message': 'The provided token is invalid or has expired'
            }), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated


def optional_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        current_user = None
        
        if token:
            current_user = AuthService.verify_token(token)
        
        return f(current_user, *args, **kwargs)
    
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({
                'error': 'Authentication required',
                'message': 'Please provide a valid authentication token'
            }), 401
        
        current_user = AuthService.verify_token(token)
        
        if not current_user:
            return jsonify({
                'error': 'Invalid authentication token',
                'message': 'The provided token is invalid or has expired'
            }), 401
        
        if not current_user.is_admin():
            return jsonify({
                'error': 'Insufficient permissions',
                'message': 'Only administrators can perform this action'
            }), 403
        
        return f(current_user, *args, **kwargs)
    
    return decorated