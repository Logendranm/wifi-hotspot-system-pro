from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify, flash, send_file
from models import User, Plan, Voucher, Session as UserSession, Payment, get_db_connection
from utils import log_action, generate_voucher_code, format_data_size, format_time_duration
import csv
import io
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    # Get statistics
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # User stats
    cursor.execute("SELECT COUNT(*) as total_users FROM users WHERE role = 'user'")
    user_stats = cursor.fetchone()
    
    cursor.execute("SELECT COUNT(*) as active_users FROM users WHERE role = 'user' AND status = 'active'")
    active_users = cursor.fetchone()
    
    # Session stats
    cursor.execute("SELECT COUNT(*) as active_sessions FROM sessions WHERE status = 'active'")
    session_stats = cursor.fetchone()
    
    # Revenue stats
    revenue_stats = Payment.get_revenue_stats()
    
    # Voucher stats
    cursor.execute("SELECT COUNT(*) as total_vouchers, SUM(status = 'unused') as unused_vouchers FROM vouchers")
    voucher_stats = cursor.fetchone()
    
    conn.close()
    
    stats = {
        'total_users': user_stats['total_users'],
        'active_users': active_users['active_users'],
        'active_sessions': session_stats['active_sessions'],
        'total_revenue': revenue_stats['total_revenue'] or 0,
        'total_transactions': revenue_stats['total_transactions'] or 0,
        'total_vouchers': voucher_stats['total_vouchers'] or 0,
        'unused_vouchers': voucher_stats['unused_vouchers'] or 0
    }
    
    return render_template('admin_dashboard.html', stats=stats)

@admin_bp.route('/users')
@admin_required
def manage_users():
    users = User.get_all()
    for user in users:
        user['data_balance_formatted'] = format_data_size(user['data_balance'] * 1024 * 1024)
        user['time_balance_formatted'] = format_time_duration(user['time_balance'])
    return render_template('manage_users.html', users=users)

@admin_bp.route('/users/<int:user_id>/toggle_status', methods=['POST'])
@admin_required
def toggle_user_status(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get current status
    cursor.execute("SELECT status FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    
    if user:
        new_status = 'inactive' if user['status'] == 'active' else 'active'
        cursor.execute("UPDATE users SET status = %s WHERE id = %s", (new_status, user_id))
        log_action(session['user_id'], 'user_status_change', f"Changed user {user_id} status to {new_status}")
        flash(f'User status updated to {new_status}', 'success')
    
    conn.close()
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/plans')
@admin_required
def manage_plans():
    plans = Plan.get_all()
    for plan in plans:
        plan['data_limit_formatted'] = format_data_size(plan['data_limit'] * 1024 * 1024)
        plan['time_limit_formatted'] = format_time_duration(plan['time_limit'])
    return render_template('manage_plans.html', plans=plans)

@admin_bp.route('/plans/create', methods=['POST'])
@admin_required
def create_plan():
    name = request.form.get('name')
    description = request.form.get('description')
    data_limit = float(request.form.get('data_limit', 0))
    time_limit = int(request.form.get('time_limit', 0))
    price = float(request.form.get('price'))
    validity_days = int(request.form.get('validity_days', 30))
    
    plan_id = Plan.create(name, description, data_limit, time_limit, price, validity_days)
    
    if plan_id:
        log_action(session['user_id'], 'plan_create', f"Created plan: {name}")
        flash('Plan created successfully!', 'success')
    else:
        flash('Error creating plan', 'error')
    
    return redirect(url_for('admin.manage_plans'))

@admin_bp.route('/vouchers')
@admin_required
def manage_vouchers():
    vouchers = Voucher.get_all()
    plans = Plan.get_all()
    return render_template('manage_vouchers.html', vouchers=vouchers, plans=plans)

@admin_bp.route('/vouchers/generate', methods=['POST'])
@admin_required
def generate_vouchers():
    plan_id = request.form.get('plan_id')
    quantity = int(request.form.get('quantity', 1))
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    generated_codes = []
    for _ in range(quantity):
        code = generate_voucher_code()
        cursor.execute("INSERT INTO vouchers (code, plan_id) VALUES (%s, %s)", (code, plan_id))
        generated_codes.append(code)
    
    conn.close()
    
    log_action(session['user_id'], 'vouchers_generate', f"Generated {quantity} vouchers for plan {plan_id}")
    flash(f'Generated {quantity} vouchers successfully!', 'success')
    
    return redirect(url_for('admin.manage_vouchers'))

@admin_bp.route('/sessions')
@admin_required
def view_sessions():
    sessions = UserSession.get_active_sessions()
    return render_template('sessions.html', sessions=sessions)

@admin_bp.route('/sessions/<int:session_id>/terminate', methods=['POST'])
@admin_required
def terminate_session(session_id):
    UserSession.terminate_session(session_id)
    log_action(session['user_id'], 'session_terminate', f"Terminated session: {session_id}")
    flash('Session terminated successfully', 'success')
    return redirect(url_for('admin.view_sessions'))

@admin_bp.route('/reports')
@admin_required
def reports():
    return render_template('reports.html')

@admin_bp.route('/reports/export/<report_type>')
@admin_required
def export_report(report_type):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if report_type == 'users':
        cursor.execute("""
            SELECT id, username, email, phone, status, data_balance, time_balance, created_at 
            FROM users WHERE role = 'user'
        """)
        filename = f'users_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
    elif report_type == 'payments':
        cursor.execute("""
            SELECT p.id, u.username, pl.name as plan_name, p.amount, p.payment_method, p.status, p.created_at
            FROM payments p
            JOIN users u ON p.user_id = u.id
            LEFT JOIN plans pl ON p.plan_id = pl.id
            ORDER BY p.created_at DESC
        """)
        filename = f'payments_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        
    elif report_type == 'sessions':
        cursor.execute("""
            SELECT s.id, u.username, s.device_mac, s.ip_address, s.start_time, s.end_time, 
                   s.data_used, s.time_used, s.status
            FROM sessions s
            JOIN users u ON s.user_id = u.id
            ORDER BY s.start_time DESC
        """)
        filename = f'sessions_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    else:
        flash('Invalid report type', 'error')
        return redirect(url_for('admin.reports'))
    
    data = cursor.fetchall()
    conn.close()
    
    # Create CSV file
    output = io.StringIO()
    if data:
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    
    # Create response
    mem = io.BytesIO()
    mem.write(output.getvalue().encode('utf-8'))
    mem.seek(0)
    output.close()
    
    log_action(session['user_id'], 'report_export', f"Exported {report_type} report")
    
    return send_file(
        mem,
        as_attachment=True,
        download_name=filename,
        mimetype='text/csv'
    )
