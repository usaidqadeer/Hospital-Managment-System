from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

from routers.auth import router as auth_router
from routers.doctors import router as doctors_router
from routers.patients import router as patients_router
from routers.appointments import router as appointments_router


# Create database tables
Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Hospital Management System API",
    version="1.0.0",
    description="Hospital Management System Backend using FastAPI",
)


# =========================
# CORS Configuration
# =========================

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",

    # Frontend deploy ہونے کے بعد اس کا URL یہاں add کریں:
    # "https://your-frontend.netlify.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# Routers
# =========================

app.include_router(
    auth_router,
    prefix="/auth",
    tags=["Authentication"],
)

app.include_router(
    doctors_router,
    prefix="/doctors",
    tags=["Doctors"],
)

app.include_router(
    patients_router,
    prefix="/patients",
    tags=["Patients"],
)

app.include_router(
    appointments_router,
    prefix="/appointments",
    tags=["Appointments"],
)


# =========================
# Root Route
# =========================

@app.get("/")
def root():
    return {
        "status": "success",
        "message": "Hospital Management System API is running successfully",
        "docs": "/docs",
    }


# =========================
# Health Check
# =========================

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Hospital Management System API",
    }