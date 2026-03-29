from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.db import get_db
from models.insurance_model import InsuranceRecord
from schemas.insurance import InsuranceCreate, InsuranceOut, InsuranceVerify
from datetime import date
import random

router = APIRouter()

def gen_insurance_id():
    return f"INS-{random.randint(100000, 999999)}"

@router.get("/patient/{patient_id}", response_model=list[InsuranceOut])
async def get_patient_insurance(patient_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(InsuranceRecord).where(InsuranceRecord.patient_id == patient_id)
    )
    return result.scalars().all()

@router.post("/", response_model=InsuranceOut, status_code=201)
async def add_insurance(data: InsuranceCreate, db: AsyncSession = Depends(get_db)):
    ins = InsuranceRecord(**data.model_dump(), insurance_id=gen_insurance_id())
    db.add(ins)
    await db.commit()
    await db.refresh(ins)
    return ins

@router.post("/verify")
async def verify_insurance(data: InsuranceVerify, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(InsuranceRecord).where(
            InsuranceRecord.patient_id == data.patient_id,
            InsuranceRecord.policy_number == data.policy_number,
            InsuranceRecord.is_active == True
        )
    )
    ins = result.scalar_one_or_none()
    if not ins:
        return {"valid": False, "message": "Insurance not found or inactive"}
    today = date.today()
    if ins.coverage_start <= today <= ins.coverage_end:
        return {
            "valid": True,
            "provider": ins.provider_name,
            "plan": ins.plan_name,
            "sum_insured": ins.sum_insured,
            "covers_outpatient": ins.covers_outpatient,
            "covers_hospitalization": ins.covers_hospitalization,
            "expiry": str(ins.coverage_end)
        }
    return {"valid": False, "message": "Policy expired"}