from pydantic import BaseModel


# ==========================
# User Schema
# ==========================

# ==========================
# User Schema
# ==========================

class UserCreate(BaseModel):

    username: str

    password: str

    role: str = "patient"

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


# ==========================
# Doctor Schema
# ==========================

class DoctorCreate(BaseModel):
    name: str
    specialization: str
    phone: str


class DoctorResponse(BaseModel):
    id: int
    name: str
    specialization: str
    phone: str

    class Config:
        from_attributes = True


# ==========================
# Patient Schema
# ==========================

class PatientCreate(BaseModel):
    name: str
    age: int
    gender: str
    disease: str


class PatientResponse(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    disease: str

    class Config:
        from_attributes = True


# ==========================
# Doctor Info Schema
# ==========================

class DoctorInfo(BaseModel):
    id: int
    name: str
    specialization: str

    class Config:
        from_attributes = True


# ==========================
# Patient Info Schema
# ==========================

class PatientInfo(BaseModel):
    id: int
    name: str
    age: int

    class Config:
        from_attributes = True


# ==========================
# Appointment Schema
# ==========================

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    date: str
    time: str


class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    date: str
    time: str

    doctor: DoctorInfo
    patient: PatientInfo

    class Config:
        from_attributes = True