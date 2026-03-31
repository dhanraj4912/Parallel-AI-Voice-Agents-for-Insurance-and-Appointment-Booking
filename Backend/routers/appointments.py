from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.db import get_db
from models.appointment import Appointment
from models.doctor import Doctor
from schemas.appointment import AppointmentCreate, AppointmentOut, AppointmentUpdate, SlotRequest
from datetime import date
import random

router = APIRouter()

def gen_appt_id():
    return f"APT-{random.randint(100000, 999999)}"

@router.get("/", response_model=list[AppointmentOut])
async def list_appointments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Appointment).order_by(Appointment.created_at.desc()))
    return result.scalars().all()

@router.get("/patient/{patient_id}", response_model=list[AppointmentOut])
async def appointments_by_patient(patient_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Appointment).where(Appointment.patient_id == patient_id)
    )
    return result.scalars().all()

@router.post("/available-slots")
async def get_available_slots(data: SlotRequest, db: AsyncSession = Depends(get_db)):
    doctor = await db.get(Doctor, data.doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")

    day_name = data.appointment_date.strftime("%A")
    if day_name not in (doctor.available_days or []):
        return {"available_slots": [], "message": f"Doctor not available on {day_name}"}

    booked = await db.execute(
        select(Appointment.appointment_time).where(
            Appointment.doctor_id == data.doctor_id,
            Appointment.appointment_date == data.appointment_date,
            Appointment.status != "cancelled"
        )
    )
    booked_times = {r[0] for r in booked.all()}
    free_slots = [s for s in (doctor.available_slots or []) if s not in booked_times]
    return {"available_slots": free_slots, "doctor": doctor.full_name, "date": str(data.appointment_date)}

@router.post("/", response_model=AppointmentOut, status_code=201)
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

    appt = Appointment(**data.model_dump(), appointment_id=gen_appt_id(), status="pending")
    db.add(appt)
    await db.commit()
    await db.refresh(appt)
    return appt

# ✅ IMPORTANT: patient-approve MUST come BEFORE /{appt_id}
@router.patch("/patient-approve/{appt_id}")
async def patient_approve_appointment(
    appt_id: int,
    action: str = Query(..., description="'approve' or 'reject'"),
    db: AsyncSession = Depends(get_db)
):
    appt = await db.get(Appointment, appt_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if action == "approve":
        appt.status = "confirmed"
    elif action == "reject":
        appt.status = "cancelled"
    else:
        raise HTTPException(status_code=400, detail="Action must be 'approve' or 'reject'")

    await db.commit()
    await db.refresh(appt)
    return {
        "message": f"Appointment {action}d successfully",
        "status": appt.status,
        "appointment_id": appt.appointment_id
    }

# ✅ Generic /{appt_id} comes LAST
@router.patch("/{appt_id}", response_model=AppointmentOut)
async def update_appointment(appt_id: int, data: AppointmentUpdate, db: AsyncSession = Depends(get_db)):
    appt = await db.get(Appointment, appt_id)
    if not appt:
        raise HTTPException(status_code=404, detail="Appointment not found")
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(appt, field, value)
    await db.commit()
    await db.refresh(appt)
    return appt