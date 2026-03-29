from pydantic import BaseModel
from datetime import date
from typing import Optional

class InsuranceCreate(BaseModel):
    patient_id: int
    provider_name: str
    policy_number: str
    plan_name: Optional[str] = None
    sum_insured: float
    premium_amount: Optional[float] = None
    coverage_start: date
    coverage_end: date
    covers_hospitalization: bool = True
    covers_outpatient: bool = False

class InsuranceOut(InsuranceCreate):
    id: int
    insurance_id: str
    is_active: bool

    class Config:
        from_attributes = True

class InsuranceVerify(BaseModel):
    patient_id: int
    policy_number: str