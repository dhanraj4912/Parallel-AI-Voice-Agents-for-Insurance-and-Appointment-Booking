from app.database.connection import get_db_connection
from app.database.queries import GET_PATIENT_DETAILS,GET_MEDICAL_HISTORY

def get_patient_details(user_id):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(GET_PATIENT_DETAILS,(user_id,))

    data = cur.fetchone()

    cur.close()
    conn.close()

    return data


def get_medical_history(user_id):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(GET_MEDICAL_HISTORY,(user_id,))

    data = cur.fetchone()

    cur.close()
    conn.close()

    return data