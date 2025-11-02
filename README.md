# 🌟 Miracle Hotels

A Django web application for managing hotel data, built with PostgreSQL, responsive design, and import/export programs.

---

## 🚀 Features

- 🏨 Hotel data management with custom admin panel
- 📥 CSV import/export with timestamped filenames
- ✅ Validation and error handling for clean data workflows
- 🔍 Display enhancements in the admin interface
- 🔐 Secure environment setup using `.env` and `python-decouple`

---

## 🛠️ Tech Stack

- **Backend**: Django 5.2, Python 3.10
- **Database**: PostgreSQL
- **Frontend**: Bootstrap (responsive design)
- **Environment**: `virtualenvwrapper`, `.env` secrets, `python-decouple`

---

## 📦 Setup Instructions

### 1. Clone the repo

git clone https://github.com/mymabc/miraclehotels.git
cd miraclehotels

### 2. Create and activate virtual environment

mkvirtualenv miraclehotels

### 3. Install dependencies

pip install -r requirements.txt

### 4. Create .env file

DB_NAME=miraclehotels
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

### 5. Run migrations and start server

python manage.py migrate
python manage.py runserver

### 6. Import/Export Scripts



