from flask import Blueprint, request, jsonify

from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Invalid request',
                'message': 'Request body must contain valid JSON'
            }), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'error': 'Missing required fields',
                'message': 'Username and password are required'
            }), 400
        
        user = AuthService.create_user(username, password)
        
        return jsonify({
            'message': 'User created successfully',
            'user': user.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({
            'error': 'Validation error',
            'message': str(e)
        }), 400
    
    except Exception as e:
        return jsonify({
            'error': 'Registration failed',
            'message': 'An unexpected error occurred during registration'
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Invalid request',
                'message': 'Request body must contain valid JSON'
            }), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({
                'error': 'Missing required fields',
                'message': 'Username and password are required'
            }), 400
        
        token, user = AuthService.authenticate_user(username, password)
        
        if token and user:
            return jsonify({
                'message': 'Login successful',
                'token': token,
                'user': user.to_dict()
            }), 200
        else:
            return jsonify({
                'error': 'Authentication failed',
                'message': 'Invalid username or password'
            }), 401
            
    except Exception as e:
        return jsonify({
            'error': 'Login failed',
            'message': 'An unexpected error occurred during login'
        }), 500

@auth_bp.route('/verify', methods=['GET'])
def verify_token():
    try:
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({
                'error': 'Missing token',
                'message': 'Authorization token is required'
            }), 401
        
        user = AuthService.verify_token(token)
        
        if user:
            return jsonify({
                'message': 'Token is valid',
                'user': user.to_dict()
            }), 200
        else:
            return jsonify({
                'error': 'Invalid token',
                'message': 'The provided token is invalid or has expired'
            }), 401
            
    except Exception as e:
        return jsonify({
            'error': 'Token verification failed',
            'message': 'An unexpected error occurred during token verification'
        }), 500

@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    try:
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({
                'error': 'Missing token',
                'message': 'Authorization token is required'
            }), 401
        
        user = AuthService.verify_token(token)
        
        if user:
            return jsonify({
                'user': user.to_dict()
            }), 200
        else:
            return jsonify({
                'error': 'Invalid token',
                'message': 'The provided token is invalid or has expired'
            }), 401
            
    except Exception as e:
        return jsonify({
            'error': 'Profile retrieval failed',
            'message': 'An unexpected error occurred while retrieving profile'
        }), 500

@auth_bp.route('/permissions', methods=['GET'])
def get_user_permissions():
    try:
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({
                'error': 'Missing token',
                'message': 'Authorization token is required'
            }), 401
        
        user = AuthService.verify_token(token)
        
        if user:
            return jsonify({
                'permissions': {
                    'can_view_stations': user.can_view_stations(),
                    'can_manage_stations': user.can_manage_stations(),
                    'is_admin': user.is_admin()
                },
                'role': user.role
            }), 200
        else:
            return jsonify({
                'error': 'Invalid token',
                'message': 'The provided token is invalid or has expired'
            }), 401
            
    except Exception as e:
        return jsonify({
            'error': 'Permission check failed',
            'message': 'An unexpected error occurred while checking permissions'
        }), 500