🤖 AI Voice Agent
Natural language appointment booking via voice or text

Groq Whisper STT + LLaMA 3 tool-calling agent

Tools: lookup_patient, get_doctors, get_available_slots, book_appointment, check_insurance

Conversation history with automatic 10-message trimming

👨‍⚕️ Admin Dashboard
Full CRUD for patients, doctors, appointments, insurance

Role-based access control (Admin / Patient)

🧑‍💻 Patient Portal
View appointments, book new ones, check insurance

🔐 Auth
JWT login, role-aware routing, Axios auto-headers

📁 Project Structure
text
voicecare/
├── Backend/
│   ├── main.py
│   ├── database.py
│   ├── auth.py
│   ├── .env
│   ├── models/         # patient, doctor, appointment, insurance, user
│   ├── routes/         # auth, admin, portal, voice
│   └── services/
│       └── voice_agent.py
└── Frontend/
    └── src/
        ├── context/AuthContext.jsx
        ├── pages/      # Login, AdminDashboard, PatientDashboard
        └── components/ # VoiceAgent
⚡ Quick Start
Backend
bash
cd Backend
python -m venv venv && venv\Scripts\activate
pip install -r requirements.txt
# Create .env (see below)
alembic upgrade head
uvicorn main:app --reload --port 8000
.env
text
SECRET_KEY=your_super_secret_jwt_key_here_min_32_chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
GROQ_API_KEY=gsk_your_groq_api_key_here
