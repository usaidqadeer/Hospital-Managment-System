from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import auth

from database import get_db


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)



# ==========================
# Admin Dashboard
# ==========================

@router.get("/admin")
def admin_dashboard(
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):

    auth.check_role(
        current_user,
        "admin"
    )


    total_users = db.query(
        models.User
    ).count()


    total_doctors = db.query(
        models.Doctor
    ).count()


    total_patients = db.query(
        models.Patient
    ).count()


    total_appointments = db.query(
        models.Appointment
    ).count()


    return {

        "dashboard": "Admin Dashboard",

        "total_users": total_users,

        "total_doctors": total_doctors,

        "total_patients": total_patients,

        "total_appointments": total_appointments

    }




# ==========================
# Doctor Dashboard
# ==========================

@router.get("/doctor")
def doctor_dashboard(
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):

    auth.check_role(
        current_user,
        "doctor"
    )


    doctor = db.query(
        models.Doctor
    ).filter(
        models.Doctor.name == current_user["username"]
    ).first()



    if not doctor:

        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )



    appointments = db.query(
        models.Appointment
    ).filter(
        models.Appointment.doctor_id == doctor.id
    ).all()



    return {

        "dashboard": "Doctor Dashboard",

        "doctor_name": doctor.name,

        "total_appointments": len(appointments),

        "appointments": [

            {
                "id": appointment.id,
                "patient_id": appointment.patient_id,
                "date": appointment.date,
                "time": appointment.time
            }

            for appointment in appointments

        ]

    }




# ==========================
# Patient Dashboard
# ==========================

@router.get("/patient")
def patient_dashboard(
    db: Session = Depends(get_db),
    current_user = Depends(auth.get_current_user)
):

    auth.check_role(
        current_user,
        "patient"
    )



    patient = db.query(
        models.Patient
    ).filter(
        models.Patient.name == current_user["username"]
    ).first()



    if not patient:

        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )



    appointments = db.query(
        models.Appointment
    ).filter(
        models.Appointment.patient_id == patient.id
    ).all()



    return {

        "dashboard": "Patient Dashboard",

        "patient_name": patient.name,

        "total_appointments": len(appointments),


        "appointments": [

            {

                "id": appointment.id,

                "doctor_id": appointment.doctor_id,

                "date": appointment.date,

                "time": appointment.time

            }

            for appointment in appointments

        ]

    }