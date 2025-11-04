from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os

from config import Config
from auth import auth_bp
from user import user_bp
from admin import admin_bp


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object(Config)

    CORS(app)
    jwt = JWTManager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Upload folder setup
    upload_folder = app.config.get('UPLOAD_FOLDER', 'uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    return app


# gunicorn entry
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
