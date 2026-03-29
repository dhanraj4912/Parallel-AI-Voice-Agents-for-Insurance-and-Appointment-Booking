from sqlalchemy import Column, Integer, String, Float, JSON
from database.db import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    doctor_id = Column(String(20), unique=True, index=True)
    full_name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False)
    qualification = Column(String(200), nullable=True)
    phone = Column(String(15), nullable=True)
    email = Column(String(100), nullable=True)
    available_days = Column(JSON, default=list)
    available_slots = Column(JSON, default=list)
    consultation_fee = Column(Float, default=500.0)
    rating = Column(Float, default=4.5)