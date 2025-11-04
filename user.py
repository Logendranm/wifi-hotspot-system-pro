from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify, flash
from models import User, Plan, Session as UserSession, Payment
from utils import log_action, format_data_size, format_time_duration

user_bp = Blueprint('user', __name__)


# ----------------------------------------------------------
# LOGIN REQUIRED DECORATOR
# ----------------------------------------------------------
def login_required(f):
    """Ensure user is logged in before accessing protected routes."""
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to continue.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function


# ----------------------------------------------------------
# USER DASHBOARD
# ----------------------------------------------------------
@user_bp.route('/dashboard')
@login_required
def dashboard():
    user = User.get_by_id(session['user_id'])
    if not user:
        session.clear()
        flash('Session expired. Please login again.', 'error')
        return redirect(url_for('auth.login'))

    # Format balances for display
    user['data_balance_formatted'] = format_data_size(user.get('data_balance', 0) * 1024 * 1024)
    user['time_balance_formatted'] = format_time_duration(user.get('time_balance', 0))

    return render_template('user_dashboard.html', user=user)


# ----------------------------------------------------------
# VIEW AVAILABLE PLANS
# ----------------------------------------------------------
@user_bp.route('/plans')
@login_required
def view_plans():
    plans = Plan.get_all() or []
    for plan in plans:
        plan['data_limit_formatted'] = format_data_size(plan.get('data_limit', 0) * 1024 * 1024)
        plan['time_limit_formatted'] = format_time_duration(plan.get('time_limit', 0))
    return render_template('plans.html', plans=plans)


# ----------------------------------------------------------
# RECHARGE PLAN
# ----------------------------------------------------------
@user_bp.route('/recharge', methods=['POST'])
@login_required
def recharge():
    plan_id = request.form.get('plan_id')
    payment_method = request.form.get('payment_method', 'online')

    if not plan_id:
        flash('No plan selected.', 'error')
        return redirect(url_for('user.view_plans'))

    plan = Plan.get_by_id(plan_id)
    if not plan:
        flash('Invalid plan selected.', 'error')
        return redirect(url_for('user.view_plans'))

    user_id = session['user_id']

    try:
        # Create payment record
        Payment.create(user_id, plan['price'], payment_method, plan_id)

        # Add balance to user
        User.update_balance(user_id, plan['data_limit'], plan['time_limit'])

        log_action(user_id, 'recharge', f"Recharged with plan: {plan['name']}")
        flash(f"Successfully recharged with {plan['name']}!", 'success')

    except Exception as e:
        log_action(user_id, 'recharge_error', f"Recharge failed: {e}")
        flash('Recharge failed. Please try again.', 'error')

    return redirect(url_for('user.dashboard'))


# ----------------------------------------------------------
# START SESSION (AJAX)
# ----------------------------------------------------------
@user_bp.route('/start_session', methods=['POST'])
@login_required
def start_session():
    user_id = session['user_id']
    device_mac = request.form.get('device_mac', 'unknown')
    ip_address = request.remote_addr

    user = User.get_by_id(user_id)
    if not user:
        return jsonify({'success': False, 'message': 'User not found'})

    if user.get('data_balance', 0) <= 0 and user.get('time_balance', 0) <= 0:
        return jsonify({'success': False, 'message': 'Insufficient balance'})

    try:
        session_id = UserSession.create(user_id, device_mac, ip_address)
        log_action(user_id, 'session_start', f"Started session: {session_id}")
        return jsonify({'success': True, 'session_id': session_id})
    except Exception as e:
        log_action(user_id, 'session_error', f"Failed to start session: {e}")
        return jsonify({'success': False, 'message': 'Could not start session'})


# ----------------------------------------------------------
# CHECK BALANCE (AJAX)
# ----------------------------------------------------------
@user_bp.route('/check_balance')
@login_required
def check_balance():
    user = User.get_by_id(session['user_id'])
    if not user:
        return jsonify({'success': False, 'message': 'User not found'})

    return jsonify({
        'success': True,
        'data_balance': user.get('data_balance', 0),
        'time_balance': user.get('time_balance', 0),
        'data_balance_formatted': format_data_size(user.get('data_balance', 0) * 1024 * 1024),
        'time_balance_formatted': format_time_duration(user.get('time_balance', 0))
    })
