from fastapi import APIRouter,HTTPException
from app.database.connection import get_db_connection
from app.schemas.models import LoginRequest

router = APIRouter()

@router.post("/login")

def login(request:LoginRequest):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM sp_login_user(%s,%s)",
        (request.email,request.password)
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    if user:

        return {"user_id":user[0]}

    raise HTTPException(status_code=401,detail="Invalid credentials")