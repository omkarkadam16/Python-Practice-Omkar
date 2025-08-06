from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from passlib.hash import bcrypt
import os
from pathlib import Path

from StartUps.local_services_app.app import database, models

# Create FastAPI app
app = FastAPI()

# Fix static path using absolute directory
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# Mount static files and templates
templates = Jinja2Templates(directory=TEMPLATES_DIR)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Create database tables
models.Base.metadata.create_all(bind=database.engine)

# DB session dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================
# ✅ HOME PAGE
# ============================
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ============================
# ✅ USER REGISTRATION
# ============================
@app.get("/register")
def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register")
def register_user(
    request: Request,
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    hashed_password = bcrypt.hash(password)
    user = models.User(name=name, email=email, password=hashed_password)
    db.add(user)
    db.commit()
    return templates.TemplateResponse("index.html", {"request": request, "message": "Registered successfully!"})

# ============================
# ✅ USER LOGIN
# ============================
@app.get("/login")
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not bcrypt.verify(password, user.password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie("user_id", user.id)
    return response

# ============================
# ✅ USER DASHBOARD
# ============================
@app.get("/dashboard")
def dashboard(request: Request):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/providers")
def list_providers(request: Request, db: Session = Depends(get_db)):
    providers = db.query(models.Provider).all()
    return templates.TemplateResponse("provider_list.html", {"request": request, "providers": providers})


@app.get("/book/{provider_id}")
def book_provider(provider_id: int, request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    # Create a new booking
    booking = models.Booking(user_id=int(user_id), provider_id=provider_id)
    db.add(booking)
    db.commit()

@app.get("/my-bookings")
def my_bookings(request: Request, db: Session = Depends(get_db)):
    user_id = request.cookies.get("user_id")
    if not user_id:
        return RedirectResponse(url="/login", status_code=302)

    bookings = db.query(models.Booking).filter(models.Booking.user_id == int(user_id)).all()
    return templates.TemplateResponse("my_bookings.html", {"request": request, "bookings": bookings})

