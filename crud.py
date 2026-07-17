from sqlalchemy.orm import Session
import models
import schemas


# ==========================
# User CRUD
# ==========================

def create_user(db: Session, username: str, password: str):

    user = models.User(
        username=username,
        password=password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_username(
    db: Session,
    username: str
):

    return db.query(
        models.User
    ).filter(
        models.User.username == username
    ).first()



# ==========================
# Doctor CRUD
# ==========================

def create_doctor(
    db: Session,
    doctor: schemas.DoctorCreate
):

    new_doctor = models.Doctor(
        **doctor.model_dump()
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return new_doctor



def get_doctors(db: Session):

    return db.query(
        models.Doctor
    ).all()



def get_doctor(
    db: Session,
    doctor_id: int
):

    return db.query(
        models.Doctor
    ).filter(
        models.Doctor.id == doctor_id
    ).first()



def update_doctor(
    db: Session,
    doctor_id: int,
    doctor: schemas.DoctorCreate
):

    db_doctor = get_doctor(
        db,
        doctor_id
    )

    if not db_doctor:
        return None


    db_doctor.name = doctor.name
    db_doctor.specialization = doctor.specialization
    db_doctor.phone = doctor.phone


    db.commit()
    db.refresh(db_doctor)

    return db_doctor



def delete_doctor(
    db: Session,
    doctor_id: int
):

    doctor = get_doctor(
        db,
        doctor_id
    )

    if doctor:
        db.delete(doctor)
        db.commit()

    return doctor




# ==========================
# Patient CRUD
# ==========================

def create_patient(
    db: Session,
    patient: schemas.PatientCreate
):

    new_patient = models.Patient(
        **patient.model_dump()
    )


    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient



def get_patients(db: Session):

    return db.query(
        models.Patient
    ).all()



def get_patient(
    db: Session,
    patient_id: int
):

    return db.query(
        models.Patient
    ).filter(
        models.Patient.id == patient_id
    ).first()



def update_patient(
    db: Session,
    patient_id: int,
    patient: schemas.PatientCreate
):

    db_patient = get_patient(
        db,
        patient_id
    )


    if not db_patient:
        return None


    db_patient.name = patient.name
    db_patient.age = patient.age
    db_patient.gender = patient.gender
    db_patient.disease = patient.disease


    db.commit()
    db.refresh(db_patient)

    return db_patient



def delete_patient(
    db: Session,
    patient_id: int
):

    patient = get_patient(
        db,
        patient_id
    )


    if patient:
        db.delete(patient)
        db.commit()


    return patient




# ==========================
# Appointment CRUD
# ==========================

def create_appointment(
    db: Session,
    appointment: schemas.AppointmentCreate
):

    new_appointment = models.Appointment(
        **appointment.model_dump()
    )


    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)


    return new_appointment



def get_appointments(
    db: Session
):

    return db.query(
        models.Appointment
    ).all()



def get_appointment(
    db: Session,
    appointment_id: int
):

    return db.query(
        models.Appointment
    ).filter(
        models.Appointment.id == appointment_id
    ).first()



def update_appointment(
    db: Session,
    appointment_id: int,
    appointment: schemas.AppointmentCreate
):

    db_appointment = get_appointment(
        db,
        appointment_id
    )


    if not db_appointment:
        return None


    db_appointment.patient_id = appointment.patient_id
    db_appointment.doctor_id = appointment.doctor_id
    db_appointment.date = appointment.date
    db_appointment.time = appointment.time


    db.commit()
    db.refresh(db_appointment)


    return db_appointment



def delete_appointment(
    db: Session,
    appointment_id: int
):

    appointment = get_appointment(
        db,
        appointment_id
    )


    if appointment:
        db.delete(appointment)
        db.commit()


    return appointment