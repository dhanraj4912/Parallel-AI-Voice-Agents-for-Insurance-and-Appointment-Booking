from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
import enum
from database.db import Base

class UserRole(str, enum.Enum):
    patient = "patient"
    admin = "admin"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    phone = Column(String(15), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.patient)
    is_approved = Column(Boolean, default=False)  # Admin approves patients
    is_active = Column(Boolean, default=True)
    patient_id = Column(Integer, nullable=True)   # links to patients table after approval
    created_at = Column(DateTime(timezone=True), server_default=func.now())