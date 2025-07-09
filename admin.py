# update_admin.py
import bcrypt
from models import User
from database import SessionLocal

db = SessionLocal()
user = db.query(User).filter(User.username == "admin").first()
if user:
    user.password = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
    db.commit()
    print("Admin password updated.")
else:
    print("Admin user not found.")
db.close()
