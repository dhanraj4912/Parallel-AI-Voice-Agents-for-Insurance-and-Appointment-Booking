from fastapi import APIRouter,HTTPException
from app.database.connection import get_db_connection
from app.schemas.models import AppointmentRequest

router = APIRouter()

@router.post("/appointments")

def create_appointment(req:AppointmentRequest):

    conn = get_db_connection()
    cur = conn.cursor()

    try:

        cur.execute(
            "SELECT * FROM sp_create_appointment(%s,%s,%s,%s)",
            (req.patient_id,req.doctor_id,req.slot_id,req.reason)
        )

        appointment_id = cur.fetchone()[0]

        conn.commit()

    except Exception as e:

        conn.rollback()

        raise HTTPException(status_code=500,detail=str(e))

    finally:

        cur.close()
        conn.close()

    return {"appointment_id":appointment_id}