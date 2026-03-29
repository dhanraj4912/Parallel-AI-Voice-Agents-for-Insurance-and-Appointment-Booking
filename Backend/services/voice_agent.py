import json
import os
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from models.insurance_model import InsuranceRecord
import os
import json
from groq import AsyncGroq
from dotenv import load_dotenv

load_dotenv()
client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are VoiceCare AI, a friendly medical assistant for a clinic.
You help patients:
1. Book doctor appointments
2. Check available time slots
3. Verify their health insurance
4. Look up their patient records and past appointments

You have access to these tools:
- lookup_patient: Find patient by name, phone, or ID
- get_doctors: Get list of doctors, filter by specialization
- get_available_slots: Get free appointment slots for a doctor on a date
- book_appointment: Book an appointment for a patient with a doctor
- check_insurance: Verify insurance for a patient

Always be warm, concise and professional. Confirm details before booking.
When booking, always confirm: patient name, doctor name, date, time, and reason.
If asked about something outside medical/appointment scope, politely redirect."""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "lookup_patient",
            "description": "Look up a patient by their name, phone number, or patient ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Patient name, phone, or ID"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_doctors",
            "description": "Get available doctors, optionally filter by specialization",
            "parameters": {
                "type": "object",
                "properties": {
                    "specialization": {"type": "string", "description": "Medical specialization e.g. Cardiologist, General Physician"}
                }
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_available_slots",
            "description": "Get available appointment slots for a doctor on a specific date",
            "parameters": {
                "type": "object",
                "properties": {
                    "doctor_id": {"type": "integer"},
                    "date": {"type": "string", "description": "Date in YYYY-MM-DD format"}
                },
                "required": ["doctor_id", "date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "book_appointment",
            "description": "Book an appointment for a patient",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_id": {"type": "integer"},
                    "doctor_id": {"type": "integer"},
                    "appointment_date": {"type": "string", "description": "YYYY-MM-DD"},
                    "appointment_time": {"type": "string", "description": "HH:MM"},
                    "reason": {"type": "string"},
                    "insurance_used": {"type": "string"}
                },
                "required": ["patient_id", "doctor_id", "appointment_date", "appointment_time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_insurance",
            "description": "Check and verify a patient's insurance details",
            "parameters": {
                "type": "object",
                "properties": {
                    "patient_id": {"type": "integer"}
                },
                "required": ["patient_id"]
            }
        }
    }
]


class VoiceAgentService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.history = [{"role": "system", "content": SYSTEM_PROMPT}]

    async def _run_tool(self, name: str, args: dict) -> str:
        try:
            if name == "lookup_patient":
                q = args["query"]
                result = await self.db.execute(
                    select(Patient).where(
                        or_(Patient.full_name.ilike(f"%{q}%"),
                            Patient.phone.ilike(f"%{q}%"),
                            Patient.patient_id.ilike(f"%{q}%"))
                    )
                )
                patients = result.scalars().all()
                if not patients:
                    return json.dumps({"found": False, "message": "No patient found"})
                return json.dumps([{
                    "id": p.id, "patient_id": p.patient_id,
                    "name": p.full_name, "phone": p.phone,
                    "dob": str(p.date_of_birth), "blood_group": p.blood_group
                } for p in patients])

            elif name == "get_doctors":
                spec = args.get("specialization", "")
                query = select(Doctor)
                if spec:
                    query = query.where(Doctor.specialization.ilike(f"%{spec}%"))
                result = await self.db.execute(query)
                doctors = result.scalars().all()
                return json.dumps([{
                    "id": d.id, "doctor_id": d.doctor_id, "name": d.full_name,
                    "specialization": d.specialization,
                    "available_days": d.available_days,
                    "fee": d.consultation_fee, "rating": d.rating
                } for d in doctors])

            elif name == "get_available_slots":
                doctor_id = args["doctor_id"]
                appt_date = date.fromisoformat(args["date"])
                doctor = await self.db.get(Doctor, doctor_id)
                if not doctor:
                    return json.dumps({"error": "Doctor not found"})
                day = appt_date.strftime("%A")
                if day not in (doctor.available_days or []):
                    return json.dumps({"slots": [], "message": f"Not available on {day}"})
                booked = await self.db.execute(
                    select(Appointment.appointment_time).where(
                        Appointment.doctor_id == doctor_id,
                        Appointment.appointment_date == appt_date,
                        Appointment.status != "cancelled"
                    )
                )
                booked_set = {r[0] for r in booked.all()}
                free = [s for s in (doctor.available_slots or []) if s not in booked_set]
                return json.dumps({"slots": free, "doctor": doctor.full_name, "date": args["date"]})

            elif name == "book_appointment":
                existing = await self.db.execute(
                    select(Appointment).where(
                        Appointment.doctor_id == args["doctor_id"],
                        Appointment.appointment_date == date.fromisoformat(args["appointment_date"]),
                        Appointment.appointment_time == args["appointment_time"],
                        Appointment.status != "cancelled"
                    )
                )
                if existing.scalar_one_or_none():
                    return json.dumps({"success": False, "message": "Slot already taken"})
                appt = Appointment(
                    appointment_id=f"APT-{random.randint(100000,999999)}",
                    patient_id=args["patient_id"],
                    doctor_id=args["doctor_id"],
                    appointment_date=date.fromisoformat(args["appointment_date"]),
                    appointment_time=args["appointment_time"],
                    reason=args.get("reason", "General consultation"),
                    insurance_used=args.get("insurance_used"),
                    status="confirmed"
                )
                self.db.add(appt)
                await self.db.commit()
                await self.db.refresh(appt)
                doctor = await self.db.get(Doctor, args["doctor_id"])
                return json.dumps({
                    "success": True,
                    "appointment_id": appt.appointment_id,
                    "doctor": doctor.full_name if doctor else "Unknown",
                    "date": args["appointment_date"],
                    "time": args["appointment_time"],
                    "status": "confirmed"
                })

            elif name == "check_insurance":
                result = await self.db.execute(
                    select(InsuranceRecord).where(
                        InsuranceRecord.patient_id == args["patient_id"],
                        InsuranceRecord.is_active == True
                    )
                )
                records = result.scalars().all()
                if not records:
                    return json.dumps({"found": False, "message": "No insurance on file"})
                today = date.today()
                return json.dumps([{
                    "insurance_id": r.insurance_id,
                    "provider": r.provider_name,
                    "policy_number": r.policy_number,
                    "plan": r.plan_name,
                    "sum_insured": r.sum_insured,
                    "valid": r.coverage_start <= today <= r.coverage_end,
                    "expiry": str(r.coverage_end),
                    "covers_outpatient": r.covers_outpatient,
                    "covers_hospitalization": r.covers_hospitalization
                } for r in records])

        except Exception as e:
            return json.dumps({"error": str(e)})

    async def chat(self, user_message: str) -> dict:
        self.history.append({"role": "user", "content": user_message})

        # Agentic loop
        while True:
            response = await client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Free Groq model
                messages=self.history,
                tools=TOOLS,
                tool_choice="auto",
                temperature=0.7
            )
            msg = response.choices[0].message

            if msg.tool_calls:
                self.history.append(msg)
                for tc in msg.tool_calls:
                    args = json.loads(tc.function.arguments)
                    result = await self._run_tool(tc.function.name, args)
                    self.history.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": result
                    })
            else:
                reply = msg.content
                self.history.append({"role": "assistant", "content": reply})
                return {"response": reply, "conversation_length": len(self.history)}


async def transcribe_audio(audio_bytes: bytes) -> str:
    """Use Groq Whisper — free"""
    import io
    from groq import AsyncGroq
    client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))
    audio_file = io.BytesIO(audio_bytes)
    audio_file.name = "recording.webm"
    transcript = await client.audio.transcriptions.create(
        model="whisper-large-v3",
        file=audio_file,
    )
    return transcript.text

async def text_to_speech(text: str) -> bytes:
    """Placeholder — TTS handled in frontend browser"""
    return text.encode("utf-8")  