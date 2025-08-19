#!/usr/bin/env bash
set -e

echo "🚀 Starting build process..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Create database tables
echo "🗄️ Setting up database..."
python -c "
import os
from app import create_app
from app.utils.database import db

print('Creating application context...')
env = os.environ.get('FLASK_ENV', 'production')
app = create_app(env)

with app.app_context():
    print('Creating database tables...')
    db.create_all()
    print('✅ Database tables created successfully!')
"

# Run seed data if needed
if [ "$FLASK_ENV" = "production" ]; then
    echo "🌱 Seeding production data..."
    python seed_data.py
fi

echo "✅ Build completed successfully!"
