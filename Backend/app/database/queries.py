LOGIN_USER = """
SELECT * FROM sp_login_user(%s,%s)
"""

GET_PATIENT_DETAILS = """
SELECT * FROM sp_get_patient_details(%s)
"""

GET_MEDICAL_HISTORY = """
SELECT * FROM sp_get_medical_history(%s)
"""

GET_SPECIALISTS = """
SELECT * FROM sp_get_specialists(%s)
"""

GET_DOCTORS = """
SELECT * FROM sp_get_doctors_by_specialists(%s)
"""

CREATE_APPOINTMENT = """
SELECT * FROM sp_create_appointment(%s,%s,%s,%s)
"""