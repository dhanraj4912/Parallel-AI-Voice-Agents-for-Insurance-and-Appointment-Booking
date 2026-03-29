from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey
from database.db import Base

class InsuranceRecord(Base):
    __tablename__ = "insurance_records"

    id = Column(Integer, primary_key=True, index=True)
    insurance_id = Column(String(30), unique=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    provider_name = Column(String(100), nullable=False)
    policy_number = Column(String(50), unique=True, nullable=False)
    plan_name = Column(String(100), nullable=True)
    sum_insured = Column(Float, nullable=False)
    premium_amount = Column(Float, nullable=True)
    coverage_start = Column(Date, nullable=False)
    coverage_end = Column(Date, nullable=False)
    covers_hospitalization = Column(Boolean, default=True)
    covers_outpatient = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)