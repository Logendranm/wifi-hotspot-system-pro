import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'wifi-hotspot-secret-key-2024'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-2024'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # Database configuration
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DATABASE = 'wifi_hotspot_db'
    
    # Upload folder for reports
    UPLOAD_FOLDER = 'reports'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
