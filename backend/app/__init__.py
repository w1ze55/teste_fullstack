from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from app.utils.database import db
from app.routes import register_blueprints
from app.middlewares.error_handlers import register_error_handlers
from config import config


def create_app(config_name=None):
    if config_name is None:
        import os
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    

    db.init_app(app)
    migrate = Migrate(app, db)
    
    cors_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    if config_name == 'production':
        cors_origins.extend([
            "https://ev-charging-frontend.onrender.com",
            "https://*.onrender.com"
        ])
    
    CORS(app, origins=cors_origins, supports_credentials=True)
    

    register_blueprints(app)
    

    register_error_handlers(app)
    

    with app.app_context():
        db.create_all()
        _create_default_admin()
    
    return app


def _create_default_admin():
    from app.models.user import User
    
    if not User.query.filter_by(username='admin').first():
        admin_user = User(username='admin', role='admin')
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()
