from app.database.connection import get_db_connection
from app.database.queries import CREATE_APPOINTMENT

def create_appointment(patient_id,doctor_id,slot_id,reason):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(CREATE_APPOINTMENT,(patient_id,doctor_id,slot_id,reason))

    appointment_id = cur.fetchone()[0]

    conn.commit()

    cur.close()
    conn.close()

    return appointment_id