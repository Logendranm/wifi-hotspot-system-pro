from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify, flash
from models import User, Plan, Session as UserSession, Payment
from utils import log_action, format_data_size, format_time_duration

user_bp = Blueprint('user', __name__)

def login_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@user_bp.route('/dashboard')
@login_required
def dashboard():
    user = User.get_by_id(session['user_id'])
    if not user:
        return redirect(url_for('auth.logout'))
    
    # Format balances for display
    user['data_balance_formatted'] = format_data_size(user['data_balance'] * 1024 * 1024)  # Convert MB to bytes
    user['time_balance_formatted'] = format_time_duration(user['time_balance'])
    
    return render_template('user_dashboard.html', user=user)

@user_bp.route('/plans')
@login_required
def view_plans():
    plans = Plan.get_all()
    for plan in plans:
        plan['data_limit_formatted'] = format_data_size(plan['data_limit'] * 1024 * 1024)
        plan['time_limit_formatted'] = format_time_duration(plan['time_limit'])
    return render_template('plans.html', plans=plans)

@user_bp.route('/recharge', methods=['POST'])
@login_required
def recharge():
    plan_id = request.form.get('plan_id')
    payment_method = request.form.get('payment_method', 'online')
    
    plan = Plan.get_by_id(plan_id)
    if not plan:
        flash('Invalid plan selected', 'error')
        return redirect(url_for('user.view_plans'))
    
    user_id = session['user_id']
    
    # Create payment record
    payment_id = Payment.create(user_id, plan['price'], payment_method, plan_id)
    
    # Add balance to user
    User.update_balance(user_id, plan['data_limit'], plan['time_limit'])
    
    log_action(user_id, 'recharge', f"Recharged with plan: {plan['name']}")
    flash(f'Successfully recharged with {plan["name"]}!', 'success')
    
    return redirect(url_for('user.dashboard'))

@user_bp.route('/start_session', methods=['POST'])
@login_required
def start_session():
    user_id = session['user_id']
    device_mac = request.form.get('device_mac', 'unknown')
    ip_address = request.remote_addr
    
    # Check if user has balance
    user = User.get_by_id(user_id)
    if user['data_balance'] <= 0 and user['time_balance'] <= 0:
        return jsonify({'success': False, 'message': 'Insufficient balance'})
    
    # Create session
    session_id = UserSession.create(user_id, device_mac, ip_address)
    log_action(user_id, 'session_start', f"Started session: {session_id}")
    
    return jsonify({'success': True, 'session_id': session_id})

@user_bp.route('/check_balance')
@login_required
def check_balance():
    user = User.get_by_id(session['user_id'])
    return jsonify({
        'data_balance': user['data_balance'],
        'time_balance': user['time_balance'],
        'data_balance_formatted': format_data_size(user['data_balance'] * 1024 * 1024),
        'time_balance_formatted': format_time_duration(user['time_balance'])
    })
