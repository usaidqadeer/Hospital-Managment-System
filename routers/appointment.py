from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
import auth
import models

from database import get_db


router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)



# ==========================
# Create Appointment
# Patient + Admin Allowed
# ==========================

@router.post("/", response_model=schemas.AppointmentResponse)
def create_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):

    if current_user["role"] not in ["admin", "patient"]:

        raise HTTPException(
            status_code=403,
            detail="Only patient or admin can create appointment"
        )


    return crud.create_appointment(
        db,
        appointment
    )



# ==========================
# Get Appointments Pagination
# Admin + Doctor Allowed
# ==========================

@router.get("/", response_model=list[schemas.AppointmentResponse])
def get_appointments(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):

    if current_user["role"] not in ["admin", "doctor"]:

        raise HTTPException(
            status_code=403,
            detail="Permission denied"
        )


    skip = (page - 1) * limit


    appointments = db.query(
        models.Appointment
    ).offset(
        skip
    ).limit(
        limit
    ).all()


    return appointments



# ==========================
# Search Appointment
# ==========================

@router.get("/search")
def search_appointment(
    date: str,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):

    appointments = db.query(
        models.Appointment
    ).filter(
        models.Appointment.date.contains(date)
    ).all()


    return appointments



# ==========================
# Get Single Appointment
# ==========================

@router.get("/{appointment_id}", response_model=schemas.AppointmentResponse)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):

    appointment = crud.get_appointment(
        db,
        appointment_id
    )


    if not appointment:

        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )


    return appointment



# ==========================
# Update Appointment
# Admin Only
# ==========================

@router.put("/{appointment_id}", response_model=schemas.AppointmentResponse)
def update_appointment(
    appointment_id: int,
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):

    auth.check_role(
        current_user,
        "admin"
    )


    updated_appointment = crud.update_appointment(
        db,
        appointment_id,
        appointment
    )


    if not updated_appointment:

        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )


    return updated_appointment



# ==========================
# Delete Appointment
# Admin Only
# ==========================

@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):

    auth.check_role(
        current_user,
        "admin"
    )


    appointment = crud.delete_appointment(
        db,
        appointment_id
    )


    if not appointment:

        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )


    return {
        "message": "Appointment deleted successfully"
    }