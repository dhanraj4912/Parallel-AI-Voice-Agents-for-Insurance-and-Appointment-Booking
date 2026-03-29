from fastapi import APIRouter, Depends, UploadFile, File
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from database.db import get_db
from services.voice_agent import VoiceAgentService, transcribe_audio, text_to_speech
from pydantic import BaseModel
import uuid

router = APIRouter()
sessions: dict[str, VoiceAgentService] = {}

class ChatRequest(BaseModel):
    session_id: str
    message: str

@router.post("/session/start")
async def start_session(db: AsyncSession = Depends(get_db)):
    session_id = str(uuid.uuid4())
    agent = VoiceAgentService(db)
    sessions[session_id] = agent
    result = await agent.chat("Hello, I just connected to VoiceCare.")
    return {"session_id": session_id, "greeting": result["response"]}

@router.post("/chat")
async def text_chat(data: ChatRequest, db: AsyncSession = Depends(get_db)):
    agent = sessions.get(data.session_id)
    if not agent:
        agent = VoiceAgentService(db)
        sessions[data.session_id] = agent
    result = await agent.chat(data.message)
    return {"session_id": data.session_id, "response": result["response"]}

@router.post("/voice-chat")
async def voice_chat(session_id: str, audio: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    audio_bytes = await audio.read()
    user_text = await transcribe_audio(audio_bytes)
    agent = sessions.get(session_id)
    if not agent:
        agent = VoiceAgentService(db)
        sessions[session_id] = agent
    result = await agent.chat(user_text)
    audio_response = await text_to_speech(result["response"])
    return Response(
        content=audio_response,
        media_type="audio/mpeg",
        headers={"X-Transcript": user_text, "X-Response-Text": result["response"][:300]}
    )

@router.delete("/session/{session_id}")
async def end_session(session_id: str):
    sessions.pop(session_id, None)
    return {"message": "Session ended"}