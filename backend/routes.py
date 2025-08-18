from flask import Blueprint, request, jsonify
from functools import wraps
from services import AuthService, StationService

# Create blueprints
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
api_bp = Blueprint('api', __name__)

# Authentication decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        current_user = AuthService.verify_token(token)
        if not current_user:
            return jsonify({'message': 'Token is invalid'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

# Authentication routes
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required'}), 400
    
    try:
        user = AuthService.create_user(data['username'], data['password'])
        return jsonify({'message': 'User created successfully'}), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Username and password are required'}), 400
    
    token, user = AuthService.authenticate_user(data['username'], data['password'])
    
    if token:
        return jsonify({'token': token, 'username': user.username}), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401

# API Routes for charging stations
@api_bp.route('/cargas', methods=['GET'])
def get_charging_stations():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    
    # Filters
    filters = {
        'type': request.args.get('type'),
        'status': request.args.get('status'),
        'state': request.args.get('state')
    }
    
    # Remove empty filters
    filters = {k: v for k, v in filters.items() if v}
    
    result = StationService.get_stations(page=page, per_page=per_page, filters=filters)
    return jsonify(result)

@api_bp.route('/cargas/<int:station_id>', methods=['GET'])
def get_charging_station(station_id):
    station = StationService.get_station_by_id(station_id)
    return jsonify(station.to_dict())

@api_bp.route('/cargas', methods=['POST'])
@token_required
def create_charging_station(current_user):
    data = request.get_json()
    
    try:
        station = StationService.create_station(data)
        return jsonify(station.to_dict()), 201
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

@api_bp.route('/cargas/<int:station_id>', methods=['PUT'])
@token_required
def update_charging_station(current_user, station_id):
    data = request.get_json()
    
    try:
        station = StationService.update_station(station_id, data)
        return jsonify(station.to_dict())
    except ValueError as e:
        return jsonify({'message': str(e)}), 400

@api_bp.route('/cargas/<int:station_id>', methods=['DELETE'])
@token_required
def delete_charging_station(current_user, station_id):
    try:
        StationService.delete_station(station_id)
        return jsonify({'message': 'Charging station deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'Failed to delete station'}), 500

# Health check
@api_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

# Error handlers
@auth_bp.errorhandler(404)
@api_bp.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Resource not found'}), 404

@auth_bp.errorhandler(500)
@api_bp.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'Internal server error'}), 500
