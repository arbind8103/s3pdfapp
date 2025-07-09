# main.py
from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from auth import authenticate_user, get_db
from s3_utils import search_files
from models import User
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
from datetime import datetime
import bcrypt

# Create FastAPI app instance
app = FastAPI()

# Configure templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Create all DB tables
Base.metadata.create_all(bind=engine)

@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...), db=Depends(get_db)):
    user = authenticate_user(db, username, password)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "msg": "Invalid credentials"})
    response = RedirectResponse("/dashboard", status_code=302)
    response.set_cookie("user", user.username)
    return response

@app.get("/logout")
def logout():
    response = RedirectResponse("/", status_code=302)
    response.delete_cookie("user")
    return response

@app.get("/dashboard")
def dashboard(request: Request, query: str = "", start_date: str = "", end_date: str = "", file_type: str = "", sort_by: str = "newest", db=Depends(get_db)):
    user = request.cookies.get("user")
    if not user:
        return RedirectResponse("/", status_code=302)
    files = search_files(query=query, start_date=start_date, end_date=end_date, file_type=file_type, sort_by=sort_by)
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "files": files,
        "query": query,
        "start_date": start_date,
        "end_date": end_date,
        "user": user
    })

@app.get("/autocomplete")
def autocomplete(prefix: str = ""):
    all_files = search_files()
    suggestions = sorted({f['name'] for f in all_files if prefix.lower() in f['name'].lower()})[:10]
    return {"suggestions": suggestions}

@app.get("/admin")
def admin_panel(request: Request, db: Session = Depends(get_db)):
    current_user = request.cookies.get("user")
    if current_user != "admin":
        return RedirectResponse("/", status_code=302)
    users = db.query(User).all()
    return templates.TemplateResponse("admin.html", {"request": request, "users": users, "user": current_user})

@app.post("/admin/add")
def add_user(request: Request, username: str = Form(...), password: str = Form(...), role: str = Form("user"), db: Session = Depends(get_db)):
    current_user = request.cookies.get("user")
    if current_user != "admin":
        return RedirectResponse("/", status_code=302)

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User(username=username, password=hashed, role=role)
    db.add(user)
    db.commit()
    return RedirectResponse("/admin", status_code=302)

@app.post("/admin/delete")
def delete_user(request: Request, user_id: int = Form(...), db: Session = Depends(get_db)):
    current_user = request.cookies.get("user")
    if current_user != "admin":
        return RedirectResponse("/", status_code=302)
    db.query(User).filter(User.id == user_id).delete()
    db.commit()
    return RedirectResponse("/admin", status_code=302)
