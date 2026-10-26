import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/survey_system')
    MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', 'survey_system')
    
    FLASK_HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
    FLASK_PORT = int(os.environ.get('FLASK_PORT', 5000))
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')

class DevelopmentConfig(Config):
    FLASK_DEBUG = True

class ProductionConfig(Config):
    FLASK_DEBUG = False

class TestingConfig(Config):
    TESTING = True
    MONGO_DB_NAME = 'survey_system_test'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}