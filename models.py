from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


# ==========================
# User Model
# ==========================

class User(Base):

    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String,
        unique=True,
        index=True
    )

    password = Column(
        String
    )

    role = Column(
        String,
        default="patient"
    )


# ==========================
# Doctor Model
# ==========================

class Doctor(Base):

    __tablename__ = "doctors"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(String)

    specialization = Column(String)

    phone = Column(String)


    appointments = relationship(
        "Appointment",
        back_populates="doctor"
    )


# ==========================
# Patient Model
# ==========================

class Patient(Base):

    __tablename__ = "patients"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(String)

    age = Column(Integer)

    gender = Column(String)

    disease = Column(String)


    appointments = relationship(
        "Appointment",
        back_populates="patient"
    )



# ==========================
# Appointment Model
# ==========================

class Appointment(Base):

    __tablename__ = "appointments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    patient_id = Column(
        Integer,
        ForeignKey("patients.id")
    )


    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id")
    )


    date = Column(String)

    time = Column(String)


    patient = relationship(
        "Patient",
        back_populates="appointments"
    )


    doctor = relationship(
        "Doctor",
        back_populates="appointments"
    )