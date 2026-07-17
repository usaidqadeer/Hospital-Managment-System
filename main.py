from fastapi import FastAPI

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



# Include Routers

app.include_router(
    auth.router
)

app.include_router(
    doctor.router
)

app.include_router(
    patient.router
)

app.include_router(
    appointment.router
)

app.include_router(
    dashboard.router
)



# Home API

@app.get("/")
def home():

    return {
        "message": "Hospital Management System API Running Successfully"
    }