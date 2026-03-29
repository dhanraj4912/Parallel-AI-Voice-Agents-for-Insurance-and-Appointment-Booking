from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from database.db import get_db
from models.patient import Patient
from schemas.patient import PatientCreate, PatientOut
import uuid, random

router = APIRouter()

def gen_patient_id():
    return f"PAT-{random.randint(10000, 99999)}"

@router.get("/", response_model=list[PatientOut])
async def list_patients(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Patient).order_by(Patient.created_at.desc()))
    return result.scalars().all()

@router.get("/search", response_model=list[PatientOut])
async def search_patients(q: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Patient).where(
            or_(
                Patient.full_name.ilike(f"%{q}%"),
                Patient.phone.ilike(f"%{q}%"),
                Patient.patient_id.ilike(f"%{q}%"),
                Patient.email.ilike(f"%{q}%")
            )
        )
    )
    return result.scalars().all()

@router.get("/{patient_id}", response_model=PatientOut)
async def get_patient(patient_id: int, db: AsyncSession = Depends(get_db)):
    patient = await db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.post("/", response_model=PatientOut, status_code=201)
async def create_patient(data: PatientCreate, db: AsyncSession = Depends(get_db)):
    patient = Patient(**data.model_dump(), patient_id=gen_patient_id())
    db.add(patient)
    await db.commit()
    await db.refresh(patient)
    return patient

@router.delete("/{patient_id}")
async def delete_patient(patient_id: int, db: AsyncSession = Depends(get_db)):
    patient = await db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    await db.delete(patient)
    await db.commit()
    return {"message": "Patient deleted"}