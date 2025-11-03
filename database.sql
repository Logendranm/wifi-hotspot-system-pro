-- Create database
CREATE DATABASE IF NOT EXISTS wifi_hotspot_db;
USE wifi_hotspot_db;

-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role ENUM('user', 'admin') DEFAULT 'user',
    status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
    data_balance DECIMAL(10,2) DEFAULT 0.00,
    time_balance INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Plans table
CREATE TABLE plans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    data_limit DECIMAL(10,2) DEFAULT 0.00,
    time_limit INT DEFAULT 0,
    price DECIMAL(8,2) NOT NULL,
    validity_days INT DEFAULT 30,
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vouchers table
CREATE TABLE vouchers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) UNIQUE NOT NULL,
    plan_id INT,
    status ENUM('unused', 'used', 'expired') DEFAULT 'unused',
    user_id INT DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    used_at TIMESTAMP NULL,
    FOREIGN KEY (plan_id) REFERENCES plans(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Sessions table
CREATE TABLE sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    device_mac VARCHAR(17),
    ip_address VARCHAR(15),
    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    end_time TIMESTAMP NULL,
    data_used DECIMAL(10,2) DEFAULT 0.00,
    time_used INT DEFAULT 0,
    status ENUM('active', 'terminated', 'expired') DEFAULT 'active',
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Payments table
CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    plan_id INT DEFAULT NULL,
    voucher_id INT DEFAULT NULL,
    amount DECIMAL(8,2) NOT NULL,
    payment_method ENUM('voucher', 'online', 'cash') DEFAULT 'voucher',
    status ENUM('pending', 'completed', 'failed') DEFAULT 'completed',
    transaction_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (plan_id) REFERENCES plans(id),
    FOREIGN KEY (voucher_id) REFERENCES vouchers(id)
);

-- Logs table
CREATE TABLE logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    details TEXT,
    ip_address VARCHAR(15),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Insert default admin user
INSERT INTO users (username, email, password_hash, role) VALUES 
('admin', 'admin@hotspot.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewF7o7oUiIZjzuM2', 'admin');

-- Insert sample plans
INSERT INTO plans (name, description, data_limit, time_limit, price, validity_days) VALUES
('Basic Plan', '1GB data with 24 hours validity', 1024.00, 1440, 50.00, 1),
('Standard Plan', '5GB data with 7 days validity', 5120.00, 10080, 200.00, 7),
('Premium Plan', '10GB data with 30 days validity', 10240.00, 43200, 500.00, 30);

-- Insert sample vouchers
INSERT INTO vouchers (code, plan_id) VALUES
('WIFI2024001', 1),
('WIFI2024002', 2),
('WIFI2024003', 3);