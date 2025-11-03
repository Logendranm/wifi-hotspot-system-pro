import bcrypt
import secrets
import string
from datetime import datetime, timedelta
from models import get_db_connection

def hash_password(password):
    """Hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed_password):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def generate_voucher_code():
    """Generate random voucher code"""
    return 'WIFI' + ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(8))

def log_action(user_id, action, details=None, ip_address=None):
    """Log user action"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO logs (user_id, action, details, ip_address) VALUES (%s, %s, %s, %s)",
        (user_id, action, details, ip_address)
    )
    conn.close()

def format_data_size(bytes_value):
    """Format bytes to human readable format"""
    if bytes_value < 1024:
        return f"{bytes_value} B"
    elif bytes_value < 1024 * 1024:
        return f"{bytes_value / 1024:.2f} KB"
    elif bytes_value < 1024 * 1024 * 1024:
        return f"{bytes_value / (1024 * 1024):.2f} MB"
    else:
        return f"{bytes_value / (1024 * 1024 * 1024):.2f} GB"

def format_time_duration(minutes):
    """Format minutes to human readable format"""
    if minutes < 60:
        return f"{minutes} min"
    elif minutes < 1440:  # 24 hours
        hours = minutes // 60
        remaining_minutes = minutes % 60
        return f"{hours}h {remaining_minutes}m"
    else:
        days = minutes // 1440
        remaining_hours = (minutes % 1440) // 60
        return f"{days}d {remaining_hours}h"
