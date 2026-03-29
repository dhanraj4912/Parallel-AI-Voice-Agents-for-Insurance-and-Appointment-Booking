from fastapi import APIRouter, HTTPException
from app.database.connection import get_db_connection

router = APIRouter()

@router.get("/patient-details/{user_id}")
def get_patient_details(user_id:int):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM sp_get_patient_details(%s)",(user_id,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        raise HTTPException(status_code=404,detail="Patient not found")

    return {
        "name":row[0],
        "date_of_birth":row[1],
        "gender":row[2],
        "contact_number":row[3],
        "medical_record_number":row[4],
        "blood_group":row[5],
        "marital_status":row[6],
        "id":row[7]
    }