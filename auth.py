# auth.py
import bcrypt
from sqlalchemy.orm import Session
from models import User

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if user and bcrypt.checkpw(password.encode(), user.password.encode()):
        return user
    return None

def get_db():
    from database import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
