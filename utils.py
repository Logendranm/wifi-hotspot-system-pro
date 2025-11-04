import os
import hashlib
import datetime
import random
import string
from werkzeug.security import generate_password_hash, check_password_hash
from models import get_db_connection


# ----------------------------------------------------------
# PASSWORD HASHING
# ----------------------------------------------------------
def hash_password(password):
    """Generate secure password hash."""
    return generate_password_hash(password)


def verify_password(password, password_hash):
    """Verify hashed password."""
    return check_password_hash(password_hash, password)


# ----------------------------------------------------------
# LOGGING USER ACTIONS
# ----------------------------------------------------------
def log_action(user_id, action, description, ip_address=None):
    """Log user or admin actions."""
    conn = get_db_connection()
    if not conn:
        print("[LOG ERROR] DB connection failed.")
        return

    cursor = conn.cursor()
    try:
        sql = """
            INSERT INTO logs (user_id, action, description, ip_address, timestamp)
            VALUES (%s, %s, %s, %s, NOW())
        """
        cursor.execute(sql, (user_id, action, description, ip_address))
        conn.commit()
    except Exception as e:
        print(f"[LOG ERROR] Failed to log action: {e}")
    finally:
        conn.close()


# ----------------------------------------------------------
# VOUCHER CODE GENERATION
# ----------------------------------------------------------
def generate_voucher_code(length=10):
    """Generate random alphanumeric voucher code."""
    characters = string.ascii_uppercase + string.digits
    code = ''.join(random.choice(characters) for _ in range(length))
    return code


# ----------------------------------------------------------
# FORMAT DATA SIZE (MB, GB)
# ----------------------------------------------------------
def format_data_size(size_in_bytes):
    """Format data size into readable MB/GB."""
    try:
        size_in_mb = size_in_bytes / (1024 * 1024)
        if size_in_mb >= 1024:
            return f"{size_in_mb / 1024:.2f} GB"
        return f"{size_in_mb:.2f} MB"
    except Exception:
        return "0 MB"


# ----------------------------------------------------------
# FORMAT TIME (SECONDS → HR:MIN)
# ----------------------------------------------------------
def format_time_duration(seconds):
    """Convert seconds to hours and minutes."""
    try:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{int(hours)}h {int(minutes)}m"
    except Exception:
        return "0h 0m"


# ----------------------------------------------------------
# REPORT GENERATION (OPTIONAL)
# ----------------------------------------------------------
def generate_report_filename(report_type):
    """Generate timestamped report filename."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{report_type}_report_{timestamp}.csv"


# ----------------------------------------------------------
# HASH UTILITY (for tokens or file names)
# ----------------------------------------------------------
def create_hash(value):
    """Create MD5 hash for any string."""
    return hashlib.md5(value.encode()).hexdigest()
