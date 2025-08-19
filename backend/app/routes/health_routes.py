from flask import Blueprint, jsonify
from datetime import datetime

from app.utils.database import db

health_bp = Blueprint('health', __name__)


@health_bp.route('/', methods=['GET'])
@health_bp.route('/check', methods=['GET'])
def health_check():
    try:
        return jsonify({
            'status': 'healthy',
            'message': 'Application is running normally',
            'timestamp': datetime.utcnow().isoformat(),
            'version': '1.0.0'
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'message': 'Application health check failed',
            'timestamp': datetime.utcnow().isoformat(),
            'error': str(e)
        }), 500


@health_bp.route('/detailed', methods=['GET'])
def detailed_health_check():
    health_data = {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0',
        'checks': {
            'database': 'unknown',
            'application': 'healthy'
        }
    }
    
    try:
        db.session.execute('SELECT 1')
        health_data['checks']['database'] = 'healthy'
    except Exception as e:
        health_data['checks']['database'] = 'unhealthy'
        health_data['status'] = 'unhealthy'
        health_data['database_error'] = str(e)
    
    if health_data['checks']['database'] == 'unhealthy':
        status_code = 503
    else:
        status_code = 200
    
    return jsonify(health_data), status_code


@health_bp.route('/ready', methods=['GET'])
def readiness_check():
    try:
        db.session.execute('SELECT 1')
        
        return jsonify({
            'status': 'ready',
            'message': 'Application is ready to serve traffic',
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        return jsonify({
            'status': 'not_ready',
            'message': 'Application is not ready to serve traffic',
            'timestamp': datetime.utcnow().isoformat(),
            'error': str(e)
        }), 503


@health_bp.route('/live', methods=['GET'])
def liveness_check():
    return jsonify({
        'status': 'alive',
        'message': 'Application is alive',
        'timestamp': datetime.utcnow().isoformat()
    }), 200