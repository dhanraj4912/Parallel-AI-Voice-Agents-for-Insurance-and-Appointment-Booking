# backend/routers/patient_portal.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.db import get_db
from models.appointment import Appointment
from models.insurance_model import InsuranceRecord
from models.doctor import Doctor
from schemas.appointment import AppointmentCreate
from datetime import date
import random

router = APIRouter()

def gen_id():
    return f"APT-{random.randint(100000, 999999)}"

@router.get("/my-appointments")
async def my_appointments(patient_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Appointment)
        .where(Appointment.patient_id == patient_id)
        .order_by(Appointment.created_at.desc())
    )
    return result.scalars().all()

@router.get("/my-insurance")
async def my_insurance(patient_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(InsuranceRecord).where(InsuranceRecord.patient_id == patient_id)
    )
    return result.scalars().all()

@router.get("/available-slots")
async def available_slots(
    doctor_id: int,
    appointment_date: str,
    db: AsyncSession = Depends(get_db)
):
    doctor = await db.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    d = date.fromisoformat(appointment_date)
    day = d.strftime("%A")
    if day not in (doctor.available_days or []):
        return {"slots": [], "message": f"Doctor not available on {day}"}
    booked = await db.execute(
        select(Appointment.appointment_time).where(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_date == d,
            Appointment.status != "cancelled"
        )
    )
    booked_set = {r[0] for r in booked.all()}
    free = [s for s in (doctor.available_slots or []) if s not in booked_set]
    return {"slots": free}

@router.post("/book-appointment", status_code=201)
async def book_appointment(data: AppointmentCreate, db: AsyncSession = Depends(get_db)):
    existing = await db.execute(
        select(Appointment).where(
            Appointment.doctor_id == data.doctor_id,
            Appointment.appointment_date == data.appointment_date,
            Appointment.appointment_time == data.appointment_time,
            Appointment.status != "cancelled"
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Slot already booked")
    appt = Appointment(**data.model_dump(), appointment_id=gen_id(), status="pending")
    db.add(appt)
    await db.commit()
    await db.refresh(appt)
    return appt

@router.post("/add-insurance", status_code=201)
async def add_insurance(data: dict, db: AsyncSession = Depends(get_db)):
    ins = InsuranceRecord(
        insurance_id=f"INS-{random.randint(100000,999999)}",
        **data
    )
    db.add(ins)
    await db.commit()
    await db.refresh(ins)
    return ins