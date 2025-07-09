# create_admin.py
import bcrypt
from models import User
from database import SessionLocal

db = SessionLocal()
hashed = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
admin = User(username="admin", password=hashed, role="admin")
db.add(admin)
db.commit()
db.close()
print("Hashed admin created.")
