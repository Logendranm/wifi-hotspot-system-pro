import pymysql
from flask import current_app
import os

# ----------------------------------------------------------
# DATABASE CONNECTION
# ----------------------------------------------------------
def get_db_connection():
    try:
        conn = pymysql.connect(
            host=os.environ.get("MYSQL_HOST", "localhost"),
            user=os.environ.get("MYSQL_USER", "root"),
            password=os.environ.get("MYSQL_PASSWORD", ""),
            database=os.environ.get("MYSQL_DATABASE", "wifi_hotspot_db"),
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        print(f"[DB ERROR] Connection failed: {e}")
        return None


# ----------------------------------------------------------
# USER MODEL
# ----------------------------------------------------------
class User:
    @staticmethod
    def get_by_id(user_id):
        conn = get_db_connection()
        if not conn:
            return None
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        conn.close()
        return result

    @staticmethod
    def get_by_username(username):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()
        return user

    @staticmethod
    def get_by_email(email):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        conn.close()
        return user

    @staticmethod
    def create(username, email, password_hash, phone=None, role='user'):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = "INSERT INTO users (username, email, password_hash, phone, role, status) VALUES (%s, %s, %s, %s, %s, 'active')"
        cursor.execute(sql, (username, email, password_hash, phone, role))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id

    @staticmethod
    def update_balance(user_id, data_limit, time_limit):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET data_balance = data_balance + %s, time_balance = time_balance + %s WHERE id = %s",
            (data_limit, time_limit, user_id),
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
        return users


# ----------------------------------------------------------
# PLAN MODEL
# ----------------------------------------------------------
class Plan:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM plans")
        plans = cursor.fetchall()
        conn.close()
        return plans

    @staticmethod
    def get_by_id(plan_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM plans WHERE id = %s", (plan_id,))
        plan = cursor.fetchone()
        conn.close()
        return plan

    @staticmethod
    def create(name, description, data_limit, time_limit, price, validity_days):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO plans (name, description, data_limit, time_limit, price, validity_days)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (name, description, data_limit, time_limit, price, validity_days))
        conn.commit()
        plan_id = cursor.lastrowid
        conn.close()
        return plan_id


# ----------------------------------------------------------
# VOUCHER MODEL
# ----------------------------------------------------------
class Voucher:
    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vouchers")
        vouchers = cursor.fetchall()
        conn.close()
        return vouchers

    @staticmethod
    def get_by_code(code):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vouchers WHERE code = %s", (code,))
        voucher = cursor.fetchone()
        conn.close()
        return voucher

    @staticmethod
    def use_voucher(code, user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE vouchers SET status = 'used', used_by = %s, used_at = NOW() WHERE code = %s",
            (user_id, code),
        )
        conn.commit()
        conn.close()


# ----------------------------------------------------------
# PAYMENT MODEL
# ----------------------------------------------------------
class Payment:
    @staticmethod
    def create(user_id, amount, method, plan_id=None, voucher_id=None):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO payments (user_id, amount, payment_method, plan_id, voucher_id, status, created_at)
            VALUES (%s, %s, %s, %s, %s, 'completed', NOW())
        """
        cursor.execute(sql, (user_id, amount, method, plan_id, voucher_id))
        conn.commit()
        payment_id = cursor.lastrowid
        conn.close()
        return payment_id

    @staticmethod
    def get_revenue_stats():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT SUM(amount) AS total_revenue, COUNT(*) AS total_transactions FROM payments WHERE status = 'completed'"
        )
        stats = cursor.fetchone()
        conn.close()
        return stats


# ----------------------------------------------------------
# SESSION MODEL
# ----------------------------------------------------------
class Session:
    @staticmethod
    def get_active_sessions():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM sessions WHERE status = 'active'")
        sessions = cursor.fetchall()
        conn.close()
        return sessions

    @staticmethod
    def create(user_id, device_mac, ip_address):
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO sessions (user_id, device_mac, ip_address, start_time, status)
            VALUES (%s, %s, %s, NOW(), 'active')
        """
        cursor.execute(sql, (user_id, device_mac, ip_address))
        conn.commit()
        session_id = cursor.lastrowid
        conn.close()
        return session_id

    @staticmethod
    def terminate_session(session_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE sessions SET status = 'terminated', end_time = NOW() WHERE id = %s",
            (session_id,),
        )
        conn.commit()
        conn.close()
