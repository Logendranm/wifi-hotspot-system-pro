import os
from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from flask_jwt_extended import create_access_token
from models import User, Plan, Voucher, Payment
from utils import verify_password, hash_password, log_action

auth_bp = Blueprint('auth', __name__)


# ----------------------------------------------------------
# INDEX / LOGIN PAGE
# ----------------------------------------------------------
@auth_bp.route('/')
def index():
    """Landing route — redirect based on session role"""
    if 'user_id' in session:
        user = User.get_by_id(session['user_id'])
        if user and user['role'] == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('user.dashboard'))
    return render_template('login.html')


# ----------------------------------------------------------
# LOGIN HANDLER
# ----------------------------------------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        login_type = request.form.get('login_type', 'password')

        if login_type == 'voucher':
            return handle_voucher_login(request.form.get('voucher_code'))

        # Try username OR email
        user = User.get_by_username(username) or User.get_by_email(username)

        if user and verify_password(password, user['password_hash']):
            if user['status'] != 'active':
                flash('Account is suspended. Please contact admin.', 'error')
                return render_template('login.html')

            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']

            log_action(user['id'], 'login', "Login successful", request.remote_addr)

            return redirect(
                url_for('admin.dashboard') if user['role'] == '_
