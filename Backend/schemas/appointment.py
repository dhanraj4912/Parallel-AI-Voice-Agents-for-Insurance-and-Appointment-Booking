from pydantic import BaseModel
from datetime import date
from typing import Optional
from models.appointment import AppointmentStatus

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_date: date
    appointment_time: str
    reason: Optional[str] = None
    insurance_used: Optional[str] = None

class AppointmentOut(AppointmentCreate):
    id: int
    appointment_id: str
    status: AppointmentStatus

    class Config:
        from_attributes = True

class AppointmentUpdate(BaseModel):
    status: Optional[AppointmentStatus] = None
    notes: Optional[str] = None

class SlotRequest(BaseModel):
    doctor_id: int
    appointment_date: date