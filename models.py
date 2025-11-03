import pymysql
from config import Config

def get_db_connection():
    """Create database connection"""
    return pymysql.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DATABASE,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

class User:
    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def get_by_email(email):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def get_by_id(user_id):
        """Fetch user by ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def create(username, email, password_hash, phone=None, role='user'):
        """Prevent duplicates before inserting"""
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
        existing = cursor.fetchone()
        if existing:
            conn.close()
            return None  # already exists

        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash, phone, role, status, created_at)
            VALUES (%s, %s, %s, %s, %s, 'active', NOW())
            """,
            (username, email, password_hash, phone, role)
        )
        user_id = cursor.lastrowid
        conn.close()
        return user_id

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def update_balance(user_id, data_balance=None, time_balance=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        if data_balance is not None:
            cursor.execute("UPDATE users SET data_balance = data_balance + %s WHERE id = %s", (data_balance, user_id))
        if time_balance is not None:
            cursor.execute("UPDATE users SET time_balance = time_balance + %s WHERE id = %s", (time_balance, user_id))
        conn.close()


class Plan:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM plans WHERE status = 'active' ORDER BY price")
        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def get_by_id(plan_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM plans WHERE id = %s", (plan_id,))
        result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def create(name, description, data_limit, time_limit, price, validity_days):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO plans (name, description, data_limit, time_limit, price, validity_days, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'active')
            """,
            (name, description, data_limit, time_limit, price, validity_days)
        )
        plan_id = cursor.lastrowid
        conn.close()
        return plan_id


class Voucher:
    @staticmethod
    def get_by_code(code):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vouchers WHERE code = %s", (code,))
        result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def use_voucher(code, user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE vouchers SET status = 'used', user_id = %s, used_at = NOW() WHERE code = %s AND status = 'unused'",
            (user_id, code)
        )
        affected_rows = cursor.rowcount
        conn.close()
        return affected_rows > 0

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.*, p.name as plan_name, u.username 
            FROM vouchers v 
            LEFT JOIN plans p ON v.plan_id = p.id 
            LEFT JOIN users u ON v.user_id = u.id 
            ORDER BY v.created_at DESC
        """)
        result = cursor.fetchall()
        conn.close()
        return result


class Session:
    @staticmethod
    def create(user_id, device_mac=None, ip_address=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO sessions (user_id, device_mac, ip_address) VALUES (%s, %s, %s)",
            (user_id, device_mac, ip_address)
        )
        session_id = cursor.lastrowid
        conn.close()
        return session_id

    @staticmethod
    def get_active_sessions():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.*, u.username 
            FROM sessions s 
            JOIN users u ON s.user_id = u.id 
            WHERE s.status = 'active' 
            ORDER BY s.start_time DESC
        """)
        result = cursor.fetchall()
        conn.close()
        return result

    @staticmethod
    def terminate_session(session_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE sessions SET status = 'terminated', end_time = NOW() WHERE id = %s",
            (session_id,)
        )
        conn.close()


class Payment:
    @staticmethod
    def create(user_id, amount, payment_method, plan_id=None, voucher_id=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO payments (user_id, plan_id, voucher_id, amount, payment_method, status, created_at) VALUES (%s, %s, %s, %s, %s, 'completed', NOW())",
            (user_id, plan_id, voucher_id, amount, payment_method)
        )
        payment_id = cursor.lastrowid
        conn.close()
        return payment_id

    @staticmethod
    def get_revenue_stats():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                COUNT(*) as total_transactions,
                SUM(amount) as total_revenue,
                AVG(amount) as avg_transaction
            FROM payments 
            WHERE status = 'completed'
        """)
        result = cursor.fetchone()
        conn.close()
        return result
