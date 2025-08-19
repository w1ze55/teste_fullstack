from flask import Blueprint, request, jsonify

from app.services.charging_station_service import ChargingStationService
from app.middlewares.auth_middleware import admin_required

stations_bp = Blueprint('stations', __name__)


@stations_bp.route('/cargas', methods=['GET'])
def get_charging_stations():
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 50, type=int), 100)
        
        filters = {}
        filter_params = ['type', 'status', 'state', 'city', 'min_power', 'max_power']
        
        for param in filter_params:
            value = request.args.get(param)
            if value:
                filters[param] = value
        
        result = ChargingStationService.get_stations_with_filters(
            page=page,
            per_page=per_page,
            filters=filters if filters else None
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve stations',
            'message': 'An unexpected error occurred while retrieving charging stations'
        }), 500


@stations_bp.route('/cargas/<int:station_id>', methods=['GET'])
def get_charging_station(station_id):
    try:
        station = ChargingStationService.get_by_id_or_404(station_id)
        return jsonify(station.to_dict()), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Station not found',
            'message': f'Charging station with ID {station_id} was not found'
        }), 404


@stations_bp.route('/cargas', methods=['POST'])
@admin_required
def create_charging_station(current_user):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Invalid request',
                'message': 'Request body must contain valid JSON'
            }), 400
        
        station = ChargingStationService.create_station(data)
        
        return jsonify({
            'message': 'Charging station created successfully',
            'station': station.to_dict()
        }), 201
        
    except ValueError as e:
        return jsonify({
            'error': 'Validation error',
            'message': str(e)
        }), 400
    
    except Exception as e:
        return jsonify({
            'error': 'Station creation failed',
            'message': 'An unexpected error occurred while creating the charging station'
        }), 500


@stations_bp.route('/cargas/<int:station_id>', methods=['PUT'])
@admin_required
def update_charging_station(current_user, station_id):
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'Invalid request',
                'message': 'Request body must contain valid JSON'
            }), 400
        
        station = ChargingStationService.update_station(station_id, data)
        
        return jsonify({
            'message': 'Charging station updated successfully',
            'station': station.to_dict()
        }), 200
        
    except ValueError as e:
        return jsonify({
            'error': 'Validation error',
            'message': str(e)
        }), 400
    
    except Exception as e:
        return jsonify({
            'error': 'Station update failed',
            'message': 'An unexpected error occurred while updating the charging station'
        }), 500


@stations_bp.route('/cargas/<int:station_id>', methods=['DELETE'])
@admin_required
def delete_charging_station(current_user, station_id):
    try:
        ChargingStationService.delete(station_id)
        
        return jsonify({
            'message': 'Charging station deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Station deletion failed',
            'message': 'An unexpected error occurred while deleting the charging station'
        }), 500


@stations_bp.route('/cargas/stats', methods=['GET'])
def get_charging_station_stats():
    try:
        stats = ChargingStationService.get_station_stats()
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve statistics',
            'message': 'An unexpected error occurred while retrieving statistics'
        }), 500


@stations_bp.route('/cargas/by-location', methods=['GET'])
def get_stations_by_location():
    try:
        state = request.args.get('state')
        city = request.args.get('city')
        
        stations = ChargingStationService.get_stations_by_location(
            state=state,
            city=city
        )
        
        return jsonify({
            'stations': stations,
            'count': len(stations)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve stations by location',
            'message': 'An unexpected error occurred while filtering stations by location'
        }), 500


@stations_bp.route('/cargas/by-status/<status>', methods=['GET'])
def get_stations_by_status(status):
    try:
        stations = ChargingStationService.get_stations_by_status(status)
        
        return jsonify({
            'stations': stations,
            'count': len(stations),
            'status': status.upper()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve stations by status',
            'message': 'An unexpected error occurred while filtering stations by status'
        }), 500


@stations_bp.route('/cargas/by-type/<charger_type>', methods=['GET'])
def get_stations_by_type(charger_type):
    try:
        stations = ChargingStationService.get_stations_by_charger_type(charger_type)
        
        return jsonify({
            'stations': stations,
            'count': len(stations),
            'charger_type': charger_type.upper()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Failed to retrieve stations by charger type',
            'message': 'An unexpected error occurred while filtering stations by charger type'
        }), 500