from .auth_routes import auth_bp
from .charging_station_routes import stations_bp
from .health_routes import health_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(stations_bp, url_prefix='/api')
    app.register_blueprint(health_bp, url_prefix='/health')


__all__ = ['register_blueprints', 'auth_bp', 'stations_bp', 'health_bp']