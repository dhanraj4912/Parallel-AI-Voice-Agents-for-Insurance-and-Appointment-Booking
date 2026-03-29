import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import asyncio
from database.db import init_db, AsyncSessionLocal
from models.doctor import Doctor
from models.patient import Patient
from models.insurance_model import InsuranceRecord
from datetime import date

async def seed():
    await init_db()
    async with AsyncSessionLocal() as db:
        doctors = [
            Doctor(doctor_id="DOC-001", full_name="Dr. Priya Sharma", specialization="General Physician",
                   qualification="MBBS, MD", phone="9811000001", email="priya@voicecare.com",
                   available_days=["Monday","Tuesday","Wednesday","Thursday","Friday"],
                   available_slots=["09:00","09:30","10:00","10:30","11:00","14:00","14:30","15:00"],
                   consultation_fee=500.0, rating=4.8),
            Doctor(doctor_id="DOC-002", full_name="Dr. Rajan Mehta", specialization="Cardiologist",
                   qualification="MBBS, DM Cardiology", phone="9811000002", email="rajan@voicecare.com",
                   available_days=["Monday","Wednesday","Friday"],
                   available_slots=["10:00","10:30","11:00","15:00","15:30","16:00"],
                   consultation_fee=1200.0, rating=4.9),
            Doctor(doctor_id="DOC-003", full_name="Dr. Sneha Gupta", specialization="Dermatologist",
                   qualification="MBBS, MD Dermatology", phone="9811000003", email="sneha@voicecare.com",
                   available_days=["Tuesday","Thursday","Saturday"],
                   available_slots=["09:00","09:30","10:00","10:30","11:00"],
                   consultation_fee=800.0, rating=4.7),
            Doctor(doctor_id="DOC-004", full_name="Dr. Amit Verma", specialization="Orthopedic",
                   qualification="MBBS, MS Ortho", phone="9811000004", email="amit@voicecare.com",
                   available_days=["Monday","Tuesday","Thursday","Friday"],
                   available_slots=["09:00","10:00","11:00","14:00","15:00","16:00"],
                   consultation_fee=1000.0, rating=4.6),
        ]
        patients = [
            Patient(patient_id="PAT-10001", full_name="Rahul Singh",
                    date_of_birth=date(1990,5,15), phone="9900001111",
                    email="rahul@email.com", blood_group="B+", address="Mathura, UP"),
            Patient(patient_id="PAT-10002", full_name="Anita Patel",
                    date_of_birth=date(1985,8,22), phone="9900002222",
                    email="anita@email.com", blood_group="O+", address="Agra, UP"),
            Patient(patient_id="PAT-10003", full_name="Vikram Rao",
                    date_of_birth=date(1978,3,10), phone="9900003333",
                    email="vikram@email.com", blood_group="A+", address="Delhi"),
        ]
        for d in doctors: db.add(d)
        for p in patients: db.add(p)
        await db.commit()

        # Add insurance for patient 1
        ins = InsuranceRecord(
            insurance_id="INS-001", patient_id=1,
            provider_name="HDFC ERGO", policy_number="HDFC-POL-123456",
            plan_name="Optima Restore", sum_insured=500000.0, premium_amount=8500.0,
            coverage_start=date(2025,1,1), coverage_end=date(2026,12,31),
            covers_hospitalization=True, covers_outpatient=True
        )
        db.add(ins)
        await db.commit()
    print("✅ Database seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed())