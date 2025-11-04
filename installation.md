# 🧠 Wi-Fi Hotspot Management System — Installation Guide

This document explains how to **set up, configure, and deploy** the Wi-Fi Hotspot Management System both **locally (XAMPP)** and on **Render Cloud**.

---

## ⚙️ 1. Prerequisites

Make sure you have installed:

* **Python 3.10+**
* **pip** (Python package manager)
* **MySQL Server** (or XAMPP)
* **Git** (for version control)
* **Render account** (for deployment)

---

## 🏗️ 2. Project Structure

```
wifi-hotspot-system/
├── app.py
├── auth.py
├── admin.py
├── user.py
├── models.py
├── utils.py
├── config.py
├── requirements.txt
├── static/
├── templates/
└── reports/
```

---

## 🧩 3. Local Setup (XAMPP / Localhost)

### Step 1. Clone the Repository

```bash
git clone https://github.com/yourusername/wifi-hotspot-system.git
cd wifi-hotspot-system
```

### Step 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3. Create MySQL Database

Open **phpMyAdmin** and create a database:

```sql
CREATE DATABASE wifi_hotspot_db;
```

Then import your SQL schema:

```bash
mysql -u root -p wifi_hotspot_db < database.sql
```

### Step 4. Configure Environment (Optional)

Create a `.env` file (optional):

```
SECRET_KEY=mysecretkey
JWT_SECRET_KEY=myjwtkey
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DATABASE=wifi_hotspot_db
UPLOAD_FOLDER=reports
```

### Step 5. Run Flask App

```bash
python app.py
```

Access the system on:
👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## ☁️ 4. Render Cloud Deployment

### Step 1. Push to GitHub

Commit your code and push to GitHub.

### Step 2. Create Render Web Service

1. Go to [https://render.com](https://render.com)
2. Click **“New → Web Service”**
3. Connect your GitHub repo
4. Set:

   * **Build Command:**

     ```
     pip install -r requirements.txt
     ```
   * **Start Command:**

     ```
     gunicorn app:app
     ```

### Step 3. Add Environment Variables

```
SECRET_KEY=yoursecret
JWT_SECRET_KEY=yourjwtsecret
MYSQL_HOST=your-mysql-host
MYSQL_USER=your-db-user
MYSQL_PASSWORD=your-db-password
MYSQL_DATABASE=wifi_hotspot_db
UPLOAD_FOLDER=reports
ADMIN_SECRET=ADMIN123
```

### Step 4. Deploy

Click **Manual Deploy → Deploy Latest Commit**
Render will install dependencies, build the app, and host it automatically.

---

## ✅ 5. Test Login

Default pages:

* `/` → Login page
* `/admin/dashboard` → Admin portal
* `/user/dashboard` → User dashboard

---

## 🧾 6. Troubleshooting

| Issue                 | Solution                                              |
| --------------------- | ----------------------------------------------------- |
| TemplateNotFound      | Ensure `templates/` folder is at project root         |
| DB Connection Error   | Check MySQL credentials in `.env` or Render variables |
| Internal Server Error | View Render Logs (`Logs` tab) for stacktrace          |
| App not starting      | Check if `gunicorn app:app` is correct in Render      |

---

**Author:** Loki
**Version:** 1.0.0
**License:** MIT
