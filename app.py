from flask import Flask, render_template
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_mysqldb import MySQL
from config import Config

# Import blueprints
from auth import auth_bp
from admin import admin_bp
from user import user_bp

# ------------------------------------------------------------
# APP INITIALIZATION
# ------------------------------------------------------------
app = Flask(__name__,
            static_folder='frontend/static',
            template_folder='frontend/templates')

# Load configuration
app.config.from_object(Config)

# Initialize extensions
CORS(app)
jwt = JWTManager(app)
mysql = MySQL(app)

# ------------------------------------------------------------
# REGISTER BLUEPRINTS
# ------------------------------------------------------------
app.register_blueprint(auth_bp, url_prefix='/')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/user')

# ------------------------------------------------------------
# DEFAULT ROUTE
# ------------------------------------------------------------
@app.route('/')
def home():
    return render_template('login.html')

# ------------------------------------------------------------
# ERROR HANDLERS (Optional but clean)
# ------------------------------------------------------------
@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html'), 500


# ------------------------------------------------------------
# MAIN ENTRY POINT
# ------------------------------------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
