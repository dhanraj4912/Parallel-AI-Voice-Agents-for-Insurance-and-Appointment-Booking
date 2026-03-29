from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional

class PatientCreate(BaseModel):
    full_name: str
    date_of_birth: date
    phone: str
    email: Optional[str] = None
    blood_group: Optional[str] = None
    address: Optional[str] = None
    medical_history: Optional[str] = None
    allergies: Optional[str] = None
    emergency_contact: Optional[str] = None

class PatientOut(PatientCreate):
    id: int
    patient_id: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True