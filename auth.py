import os
from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from flask_jwt_extended import create_access_token
from models import User, Plan, Voucher, Payment
from utils import verify_password, hash_password, log_action

auth_bp = Blueprint('auth', __name__)


# ----------------------------------------------------------
# INDEX / LOGIN PAGE
# ----------------------------------------------------------
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        login_type = request.form.get('login_type', 'password')

        # 🔹 Voucher login case
        if login_type == 'voucher':
            return handle_voucher_login(request.form.get('voucher_code'))

        # 🔹 Try username or email
        user = User.get_by_username(username) or User.get_by_email(username)

        if user and verify_password(password, user['password_hash']):
            if user['status'] != 'active':
                flash('Account is suspended. Please contact admin.', 'error')
                return render_template('login.html')

            # 🔹 Set session details
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']

            log_action(user['id'], 'login', "Login successful", request.remote_addr)

            # 🔹 Redirect based on role (✅ fixed the syntax here)
            return redirect(
                url_for('admin.dashboard') if user['role'] == 'admin' else url_for('user.dashboard')
            )

        else:
            flash('Invalid username or password', 'error')

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
        url_for('admin.dashboard') if user['role'] == 'admin' else url_for('user.dashboard')
    )

        else:
            flash('Invalid username or password', 'error')

    return render_template('login.html')


# ----------------------------------------------------------
# VOUCHER LOGIN HANDLER
# ----------------------------------------------------------
def handle_voucher_login(voucher_code):
    if not voucher_code:
        flash('Please enter voucher code', 'error')
        return render_template('login.html')

    voucher = Voucher.get_by_code(voucher_code)
    if not voucher or voucher['status'] != 'unused':
        flash('Invalid or used voucher code', 'error')
        return render_template('login.html')

    temp_username = f"voucher_{voucher_code}"
    temp_password = hash_password(voucher_code)

    try:
        user_id = User.create(
            username=temp_username,
            email=f"{temp_username}@temp.com",
            password_hash=temp_password
        )

        plan = Plan.get_by_id(voucher['plan_id'])
        if plan:
            User.update_balance(user_id, plan['data_limit'], plan['time_limit'])
            Voucher.use_voucher(voucher_code, user_id)
            Payment.create(user_id, plan['price'], 'voucher', plan['id'], voucher['id'])

        session['user_id'] = user_id
        session['username'] = temp_username
        session['role'] = 'user'

        log_action(user_id, 'voucher_login', f"Logged in with voucher: {voucher_code}")
        return redirect(url_for('user.dashboard'))

    except Exception as e:
        log_action(0, 'voucher_error', f"Voucher login failed: {e}")
        flash('Error processing voucher. Please try again.', 'error')
        return render_template('login.html')


# ----------------------------------------------------------
# USER REGISTRATION
# ----------------------------------------------------------
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')

        if User.get_by_username(username) or User.get_by_email(email):
            flash('Username or email already exists', 'error')
            return render_template('login.html')

        password_hash = hash_password(password)
        user_id = User.create(username, email, password_hash, phone)

        if user_id:
            flash('Registration successful. Please login.', 'success')
            log_action(user_id, 'register', "New user registered")
            return redirect(url_for('auth.login'))
        else:
            flash('Registration failed. Please try again.', 'error')

    return render_template('login.html')


# ----------------------------------------------------------
# SECURE ADMIN REGISTRATION (via Secret Code)
# ----------------------------------------------------------
@auth_bp.route('/admin_register', methods=['GET', 'POST'])
def admin_register():
    # ✅ Secure: use environment variable instead of hardcoded secret
    secret_code = os.environ.get("ADMIN_SECRET", "ADMIN123")

    if request.method == 'POST':
        entered_code = request.form.get('secret_code')
        if entered_code != secret_code:
            flash('Invalid secret code! Access denied.', 'error')
            return render_template('admin_register.html')

        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.get_by_username(username) or User.get_by_email(email):
            flash('Username or email already exists', 'error')
            return render_template('admin_register.html')

        password_hash = hash_password(password)
        admin_id = User.create(username, email, password_hash, role='admin')

        if admin_id:
            flash('Admin account created successfully!', 'success')
            log_action(admin_id, 'admin_register', "New admin created")
            return redirect(url_for('auth.login'))
        else:
            flash('Failed to create admin account. Try again.', 'error')

    return render_template('admin_register.html')


# ----------------------------------------------------------
# LOGOUT
# ----------------------------------------------------------
@auth_bp.route('/logout')
def logout():
    if 'user_id' in session:
        log_action(session['user_id'], 'logout', "User logged out")
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))


