from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.db import get_db
from models.patient import Patient
from pydantic import BaseModel
import os, hashlib, secrets, random
from datetime import date

router = APIRouter()


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    hashed = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    return f"{salt}:{hashed}"


def verify_password(password: str, stored_hash: str) -> bool:
    try:
        salt, hashed = stored_hash.split(":", 1)
        check = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
        return check == hashed
    except Exception:
        return False


def make_token(user_id: int, role: str) -> str:
    import base64, json
    payload = json.dumps({"id": user_id, "role": role})
    return base64.b64encode(payload.encode()).decode()


class RegisterRequest(BaseModel):
    full_name: str
    email: str
    phone: str
    password: str
    date_of_birth: str
    blood_group: str = None
    address: str = None


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register", status_code=201)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Patient).where(Patient.email == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")

    result2 = await db.execute(select(Patient).where(Patient.phone == data.phone))
    if result2.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Phone number already registered")

    hashed = hash_password(data.password)

    patient = Patient(
        patient_id=f"PAT-{random.randint(10000, 99999)}",
        full_name=data.full_name,
        email=data.email,
        phone=data.phone,
        password_hash=hashed,
        date_of_birth=date.fromisoformat(data.date_of_birth),
        blood_group=data.blood_group,
        address=data.address,
        is_approved=True,
    )
    db.add(patient)
    await db.commit()
    await db.refresh(patient)

    return {
        "message": "Registration successful! You can now login.",
        "patient_id": patient.patient_id
    }


@router.post("/login")
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    admin_email    = os.getenv("ADMIN_EMAIL",    "admin@voicecare.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")

    if data.email == admin_email and data.password == admin_password:
        return {
            "token": make_token(0, "admin"),
            "user": {
                "id": 0,
                "patient_id": "ADMIN",
                "full_name": "Administrator",
                "email": admin_email,
                "role": "admin",
                "is_approved": True
            }
        }

    result = await db.execute(select(Patient).where(Patient.email == data.email))
    patient = result.scalar_one_or_none()

    if not patient:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not patient.password_hash:
        raise HTTPException(status_code=401, detail="Password not set. Please re-register.")

    if not verify_password(data.password, patient.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not patient.is_approved:
        raise HTTPException(status_code=403, detail="Account pending admin approval")

    return {
        "token": make_token(patient.id, "patient"),
        "user": {
            "id":          patient.id,
            "patient_id":  patient.patient_id,
            "full_name":   patient.full_name,
            "email":       patient.email,
            "phone":       patient.phone,
            "blood_group": patient.blood_group,
            "role":        "patient",
            "is_approved": patient.is_approved
        }
    }