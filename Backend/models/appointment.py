from sqlalchemy import Column, Integer, String, Date, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
import enum
from database.db import Base

class AppointmentStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    completed = "completed"
    cancelled = "cancelled"

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    appointment_id = Column(String(20), unique=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    appointment_date = Column(Date, nullable=False)
    appointment_time = Column(String(10), nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.confirmed)
    reason = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    insurance_used = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())