from pydantic import BaseModel
from typing import Optional, List

class DoctorOut(BaseModel):
    id: int
    doctor_id: str
    full_name: str
    specialization: str
    qualification: Optional[str] = None
    available_days: List[str] = []
    available_slots: List[str] = []
    consultation_fee: float
    rating: float

    class Config:
        from_attributes = True