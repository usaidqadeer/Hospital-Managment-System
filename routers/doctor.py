from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
import auth
import models

from database import get_db


router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)



# ==========================
# Create Doctor (Admin Only)
# ==========================

@router.post("/", response_model=schemas.DoctorResponse)
def create_doctor(
    doctor: schemas.DoctorCreate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):

    auth.check_role(
        current_user,
        "admin"
    )


    return crud.create_doctor(
        db,
        doctor
    )



# ==========================
# Get Doctors With Pagination
# ==========================

@router.get("/", response_model=list[schemas.DoctorResponse])
def get_doctors(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):

    skip = (page - 1) * limit


    doctors = db.query(
        models.Doctor
    ).offset(
        skip
    ).limit(
        limit
    ).all()


    return doctors



# ==========================
# Search Doctor
# ==========================

@router.get("/search")
def search_doctor(
    name: str,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):

    doctors = db.query(
        models.Doctor
    ).filter(
        models.Doctor.name.contains(name)
    ).all()


    return doctors



# ==========================
# Get Single Doctor
# ==========================

@router.get("/{doctor_id}", response_model=schemas.DoctorResponse)
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):

    doctor = crud.get_doctor(
        db,
        doctor_id
    )


    if not doctor:

        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )


    return doctor



# ==========================
# Update Doctor (Admin Only)
# ==========================

@router.put("/{doctor_id}", response_model=schemas.DoctorResponse)
def update_doctor(
    doctor_id: int,
    doctor: schemas.DoctorCreate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):

    auth.check_role(
        current_user,
        "admin"
    )


    updated_doctor = crud.update_doctor(
        db,
        doctor_id,
        doctor
    )


    if not updated_doctor:

        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )


    return updated_doctor



# ==========================
# Delete Doctor (Admin Only)
# ==========================

@router.delete("/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):

    auth.check_role(
        current_user,
        "admin"
    )


    doctor = crud.delete_doctor(
        db,
        doctor_id
    )


    if not doctor:

        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )


    return {
        "message": "Doctor deleted successfully"
    }