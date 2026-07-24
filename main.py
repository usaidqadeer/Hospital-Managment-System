from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

from routers.auth import router as auth_router
from routers.doctor import router as doctors_router
from routers.patient import router as patients_router
from routers.appointment import router as appointments_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Hospital Management System API",
    version="1.0.0",
    description="Hospital Management System Backend using FastAPI",
)

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

@app.get("/")
def root():
    return {
        "status": "success",
        "message": "Hospital Management System API is running successfully",
        "docs": "/docs",
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Hospital Management System API",
    }