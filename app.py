from flask import Flask, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

from config import Config
from auth import auth_bp
from user import user_bp  
from admin import admin_bp

def create_app():
    app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
    app.config.from_object(Config)
    
    # Initialize extensions
    CORS(app)
    jwt = JWTManager(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Create upload folder if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
