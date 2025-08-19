import os
from app import create_app
from app.utils.database import db

env = os.environ.get('FLASK_ENV', 'development')
app = create_app(env)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    port = int(os.environ.get('PORT', 5000))
    debug = env == 'development'
    
    app.run(debug=debug, host='0.0.0.0', port=port)