import os
from dotenv import load_dotenv

load_dotenv()

def fix_database_url(database_url):
    """
    Fix DATABASE_URL to use psycopg3 instead of psycopg2
    """
    if database_url and database_url.startswith('postgresql://'):
        # Replace postgresql:// with postgresql+psycopg:// for psycopg3
        return database_url.replace('postgresql://', 'postgresql+psycopg://')
    return database_url

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = fix_database_url(
        os.environ.get('DATABASE_URL') or 'postgresql://postgres:postgres@localhost/charging_stations'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    @staticmethod
    def get_port():
        return int(os.environ.get('PORT', 5000))

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = fix_database_url(
        os.environ.get('DATABASE_URL') or 'sqlite:///charging_stations.db'
    )

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = fix_database_url(os.environ.get('DATABASE_URL'))

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = 'test-secret-key'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}