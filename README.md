# 💻 Wi-Fi Hotspot Management System

A **web-based Wi-Fi Hotspot Management System** built with
**HTML, CSS, JavaScript (Frontend)** and **Python Flask (Backend)** using **MySQL Database**.

This system allows administrators to manage users, plans, vouchers, payments, and monitor connections.
It provides both **admin** and **user** dashboards for full control.

---

## 🚀 Features

* 🔐 **Secure Login System** (Admin & User)
* 🎫 **Voucher-Based Access** Support
* 💰 **Internet Plan Management**
* 📊 **User Reports & Analytics**
* 🧾 **Recharge & Payment Management**
* ⚙️ **Admin Dashboard** for overall control
* 🌐 **Responsive Frontend (HTML + CSS + JS)**

---

## 🧠 Tech Stack

| Component      | Technology            |
| -------------- | --------------------- |
| **Frontend**   | HTML, CSS, JavaScript |
| **Backend**    | Python Flask          |
| **Database**   | MySQL                 |
| **Deployment** | Render Cloud Platform |
| **Server**     | Gunicorn (WSGI)       |

---

## ⚙️ Folder Structure

```
wifi-hotspot-system/
├── backend/
│   ├── app.py
│   ├── auth.py
│   ├── admin.py
│   ├── user.py
│   ├── config.py
│   ├── models.py
│   ├── utils.py
│   └── __init__.py
├── frontend/
│   ├── templates/
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   └── ...
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
├── requirements.txt
├── Procfile
└── README.md
```

---

## 🧩 Installation (Local Setup)

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/wifi-hotspot-system.git
cd wifi-hotspot-system
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate  # for Windows
source venv/bin/activate  # for Linux/Mac
```

### 3️⃣ Install Requirements

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Database

* Start **XAMPP / MySQL Server**
* Open **phpMyAdmin**
* Create a new database named:

  ```
  wifi_hotspot_db
  ```
* Import your `.sql` schema (if available) from `/backend/database/`.

Update your **config.py** (only for local testing):

```python
MYSQL_HOST = 'localhost'
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_DATABASE = 'wifi_hotspot_db'
```

### 5️⃣ Run Flask App Locally

```bash
cd backend
python app.py
```

App runs at → `http://127.0.0.1:5000/`

---

## ☁️ Deployment (Render)

### 1️⃣ Push code to GitHub

### 2️⃣ Create a New Render Web Service

* Connect your GitHub repo
* Select **Python** environment

### 3️⃣ Add Environment Variables in Render Dashboard:

```
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
ADMIN_SECRET=ADMIN123
MYSQL_HOST=your-mysql-host
MYSQL_USER=your-db-user
MYSQL_PASSWORD=your-db-password
MYSQL_DATABASE=wifi_hotspot_db
```

### 4️⃣ Build & Start Command

```
Build Command: pip install -r requirements.txt
Start Command: gunicorn backend.app:app
```

### ✅ After deployment

Render URL example:
👉 [https://wifi-hotspot-system.onrender.com](https://wifi-hotspot-system.onrender.com)

---

## 🧰 Requirements

```
Flask==3.0.3
Flask-Cors==4.0.0
Flask-JWT-Extended==4.6.0
Flask-MySQLdb==2.0.0
gunicorn==23.0.0
PyMySQL==1.1.0
cryptography==43.0.1
```

---

## 🧾 Screenshots

| Login Page                                      | Admin Dashboard                                    |
| ----------------------------------------------- | -------------------------------------------------- |
| ![Login Page](frontend/static/images/login.png) | ![Dashboard](frontend/static/images/dashboard.png) |

---

## 👨‍💻 Developed By

**Lokesh (Loki)**
Wi-Fi Hotspot Management Project — 2025
For Educational / College Project Purposes 🏫

---
