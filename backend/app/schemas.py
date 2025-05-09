from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class DoctorBase(BaseModel):
    name: str
    specialty: str
    slots_per_day: int

class DoctorCreate(DoctorBase):
    pass

class Doctor(DoctorBase):
    id: int

    class Config:
        orm_mode = True

class AppointmentBase(BaseModel):
    patient_name: str
    appointment_date: datetime
    time_slot: str

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int
    doctor_id: int
    is_cancelled: bool

    class Config:
        orm_mode = True