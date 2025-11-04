import os
from datetime import timedelta

class Config:
    # Flask secret keys
    SECRET_KEY = os.environ.get('SECRET_KEY', 'wifi-hotspot-secret-key-2024')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    # MySQL configuration (Render or Local)
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'wifi_hotspot_db')

    # Upload folder (for reports or PDFs)
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'reports')

    # Max upload file size (16 MB)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
