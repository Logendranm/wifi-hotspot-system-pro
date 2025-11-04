from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

from config import Config
from auth import auth_bp
from user import user_bp
from admin import admin_bp


def create_app():
    # ✅ templates & static folders same directoryல இருக்குது
    app = Flask(__name__, template_folder='templates', static_folder='static')
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


# ✅ Add this line so gunicorn app:app will work
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
