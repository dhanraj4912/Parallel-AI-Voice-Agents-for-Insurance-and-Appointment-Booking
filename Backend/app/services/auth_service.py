from app.database.connection import get_db_connection
from app.database.queries import LOGIN_USER

def login_user(email,password):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(LOGIN_USER,(email,password))

    user = cur.fetchone()

    cur.close()
    conn.close()

    return user