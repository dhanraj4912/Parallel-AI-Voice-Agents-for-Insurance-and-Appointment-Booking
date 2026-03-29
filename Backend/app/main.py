from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.config import Config

from app.routes import (
    auth_routes,
    langgraph_routes,
    appointment_routes
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[Config.FRONTEND_ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(langgraph_routes.router)
app.include_router(appointment_routes.router)

@app.get("/")

def root():

    return {"message":"Healthcare AI Backend Running"}