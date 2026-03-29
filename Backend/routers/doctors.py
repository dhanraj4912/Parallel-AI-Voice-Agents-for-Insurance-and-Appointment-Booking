from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.db import get_db
from models.doctor import Doctor
from schemas.doctor import DoctorOut

router = APIRouter()

@router.get("/", response_model=list[DoctorOut])
async def list_doctors(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Doctor))
    return result.scalars().all()

@router.get("/specialization/{spec}", response_model=list[DoctorOut])
async def doctors_by_specialization(spec: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Doctor).where(Doctor.specialization.ilike(f"%{spec}%"))
    )
    return result.scalars().all()

@router.get("/{doctor_id}", response_model=DoctorOut)
async def get_doctor(doctor_id: int, db: AsyncSession = Depends(get_db)):
    doctor = await db.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor