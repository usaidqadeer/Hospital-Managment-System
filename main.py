from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine
import models

from routers import auth
from routers import doctor
from routers import patient
from routers import appointment
from routers import dashboard


# Create Database Tables
models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Hospital Management System",
    version="1.0.0"
)

# =========================
# CORS Middleware
# =========================
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Include Routers
# =========================
app.include_router(auth.router)
app.include_router(doctor.router)
app.include_router(patient.router)
app.include_router(appointment.router)
app.include_router(dashboard.router)

# =========================
# Home API
# =========================
@app.get("/")
def home():
    return {
        "message": "Hospital Management System API Running Successfully"
    }