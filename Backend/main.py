from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database.db import init_db

# Import routers
from routers import patients, doctors, appointments, insurance, voice, auth

# Optional routers — load safely
try:
    from routers import patient_portal
    _has_portal = True
except ImportError:
    _has_portal = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Just initialise the DB tables — no User model needed
    await init_db()
    yield

app = FastAPI(
    title="VoiceCare AI API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Core routes
app.include_router(auth.router,         prefix="/api/auth",         tags=["Auth"])
app.include_router(patients.router,     prefix="/api/patients",     tags=["Patients"])
app.include_router(doctors.router,      prefix="/api/doctors",      tags=["Doctors"])
app.include_router(appointments.router, prefix="/api/appointments", tags=["Appointments"])
app.include_router(insurance.router,    prefix="/api/insurance",    tags=["Insurance"])
app.include_router(voice.router,        prefix="/api/voice",        tags=["Voice"])

# Patient portal routes
if _has_portal:
    app.include_router(patient_portal.router, prefix="/api/portal", tags=["Patient Portal"])

@app.get("/")
async def root():
    return {"message": "VoiceCare AI is running", "docs": "/docs"}