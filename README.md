# 📄 S3 PDF Viewer & Admin Panel (FastAPI + S3 + Uvicorn)

A secure, lightweight web application built with **FastAPI** that allows you to:
- 🔍 Search and view PDF files directly from an **S3 bucket**
- 👨‍💼 Manage users via a protected **Admin Panel**
- 📥 Download, print, and view files in the browser without storing locally
- 🔐 Secure login system with hashed passwords
- 🌐 Deployed using **Uvicorn** with optional Apache/Nginx reverse proxy

---

## 🧰 Features

- 🔑 Login system with hashed passwords (bcrypt)
- 📁 Real-time search by filename, date range, and suggestions
- 🎨 Clean UI inspired by Dribbble design
- 👩‍💼 Admin dashboard to manage users (add/delete)
- 💾 Uses SQLite (easily upgradable to PostgreSQL/MySQL)
- 🛡️ Cookie-based authentication

---

## 🚀 Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/)
- [Jinja2](https://jinja.palletsprojects.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [boto3](https://boto3.amazonaws.com/) (for AWS S3 integration)
- [bcrypt](https://pypi.org/project/bcrypt/)
- HTML + CSS for frontend

---

## 📂 Project Structure



s3pdfapp/
│
├── main.py # FastAPI routes and logic
├── auth.py # Login authentication logic
├── database.py # DB connection setup (SQLite)
├── models.py # SQLAlchemy User model
├── s3_utils.py # S3 connection + file search
│
├── templates/ # Jinja2 HTML templates
│ ├── login.html
│ ├── dashboard.html
│ └── admin.html
│
├── static/ # CSS and static assets
│ └── style.css
│
├── .env # AWS credentials & secrets (do not push to GitHub)
├── requirements.txt # List of Python dependencies
└── README.md # This file

## 2. Setup environment
uv venv       # or python -m venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt

##  Add .env file
Create .env with your AWS credentials:

AWS_ACCESS_KEY_ID=YOUR_KEY
AWS_SECRET_ACCESS_KEY=YOUR_SECRET
AWS_REGION=ap-south-1
S3_BUCKET_NAME=bills-pos
S3_PREFIX=POS/

## Run APP
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

## 🔐 Admin Panel Access

Access: http://yourserver:8000/admin

Add or delete users (except 'admin')

Role-based login (admin/user)

## 🧪 Sample Search Features
🔍 By filename (with autocomplete)

📅 Between two dates

📂 By extension/file type

🔄 Sorted (latest first)




