# 🌐 Wi-Fi Hotspot Management System — API Documentation

This document describes all **RESTful API endpoints** available for authentication, users, plans, vouchers, and reports.

---

## 🔐 Authentication Endpoints (`auth.py`)

### 1. **POST /login**

**Purpose:** Authenticate user by username & password or voucher.

**Request:**

```json
{
  "username": "john123",
  "password": "mypassword"
}
```

**Response:**

```json
{
  "success": true,
  "message": "Login successful",
  "role": "user"
}
```

---

### 2. **POST /register**

**Purpose:** Register a new user.

**Request:**

```json
{
  "username": "john123",
  "email": "john@example.com",
  "password": "mypassword",
  "phone": "9876543210"
}
```

**Response:**

```json
{
  "success": true,
  "message": "User registered successfully"
}
```

---

### 3. **POST /admin_register**

**Purpose:** Create a new admin account using a secret code.

**Request:**

```json
{
  "username": "admin",
  "email": "admin@example.com",
  "password": "123456",
  "secret_code": "ADMIN123"
}
```

**Response:**

```json
{
  "success": true,
  "message": "Admin account created"
}
```

---

## 👤 User Endpoints (`user.py`)

### 1. **GET /user/dashboard**

Displays the user dashboard page (HTML).

### 2. **GET /user/plans**

Returns all available internet plans.

**Response Example:**

```json
[
  {
    "id": 1,
    "name": "Basic Plan",
    "price": 100,
    "data_limit": "2 GB",
    "time_limit": "1h"
  }
]
```

### 3. **POST /user/recharge**

Recharge a user account using a selected plan.

**Form Data:**

```
plan_id=1
payment_method=online
```

### 4. **GET /user/check_balance**

Check user remaining data and time balance.

**Response:**

```json
{
  "success": true,
  "data_balance": 500,
  "time_balance": 3600,
  "data_balance_formatted": "500 MB",
  "time_balance_formatted": "1h 0m"
}
```

---

## 🧑‍💼 Admin Endpoints (`admin.py`)

### 1. **GET /admin/dashboard**

View admin summary (total users, sessions, vouchers, revenue).

### 2. **GET /admin/users**

List all registered users.

### 3. **POST /admin/plans/create**

Create a new data plan.

**Form Data:**

```
name=Premium Plan
data_limit=2048
time_limit=7200
price=299
validity_days=30
```

### 4. **POST /admin/vouchers/generate**

Generate new voucher codes.

**Form Data:**

```
plan_id=1
quantity=10
```

---

## 💳 Payment & Session

### **POST /user/start_session**

Start a new internet session.

**Response:**

```json
{
  "success": true,
  "session_id": 42
}
```

### **POST /admin/sessions/<id>/terminate**

Terminate an active user session.

---

## 📊 Reports (`/admin/reports`)

### **GET /admin/reports/export/users**

Export all users as CSV.

### **GET /admin/reports/export/payments**

Export all payment records as CSV.

### **GET /admin/reports/export/sessions**

Export session history as CSV.

---

## 🧠 Response Codes

| Code | Description  |
| ---- | ------------ |
| 200  | Success      |
| 400  | Bad Request  |
| 401  | Unauthorized |
| 403  | Forbidden    |
| 404  | Not Found    |
| 500  | Server Error |

---

**Base URL (Render):**
`https://your-app-name.onrender.com`

**Author:** Loki
**Version:** 1.0.0
**License:** MIT
