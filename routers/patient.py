from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import schemas
import auth
import models

from database import get_db


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)



# ==========================
# Create Patient (Admin Only)
# ==========================

@router.post("/", response_model=schemas.PatientResponse)
def create_patient(
    patient: schemas.PatientCreate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):

    auth.check_role(
        current_user,
        "admin"
    )


    return crud.create_patient(
        db,
        patient
    )



# ==========================
# Get Patients With Pagination
# ==========================

@router.get("/", response_model=list[schemas.PatientResponse])
def get_patients(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):

    skip = (page - 1) * limit


    patients = db.query(
        models.Patient
    ).offset(
        skip
    ).limit(
        limit
    ).all()


    return patients



# ==========================
# Search Patient
# ==========================

@router.get("/search")
def search_patient(
    disease: str,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):

    patients = db.query(
        models.Patient
    ).filter(
        models.Patient.disease.contains(disease)
    ).all()


    return patients



# ==========================
# Get Single Patient
# ==========================

@router.get("/{patient_id}", response_model=schemas.PatientResponse)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):

    patient = crud.get_patient(
        db,
        patient_id
    )


    if not patient:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )


    return patient



# ==========================
# Update Patient (Admin Only)
# ==========================

@router.put("/{patient_id}", response_model=schemas.PatientResponse)
def update_patient(
    patient_id: int,
    patient: schemas.PatientCreate,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):

    auth.check_role(
        current_user,
        "admin"
    )


    updated_patient = crud.update_patient(
        db,
        patient_id,
        patient
    )


    if not updated_patient:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )


    return updated_patient



# ==========================
# Delete Patient (Admin Only)
# ==========================

@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):

    auth.check_role(
        current_user,
        "admin"
    )


    patient = crud.delete_patient(
        db,
        patient_id
    )


    if not patient:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )


    return {
        "message": "Patient deleted successfully"
    }