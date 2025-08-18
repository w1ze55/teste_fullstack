from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
import os

from config import config
from models import db, User
from routes import auth_bp, api_bp

def create_app(config_name=None):
    """Application factory pattern."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    db.init_app(app)
    migrate = Migrate(app, db)
    CORS(app)
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)
    
    with app.app_context():
        db.create_all()
        
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin')
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)