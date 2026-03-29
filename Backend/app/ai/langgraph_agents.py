import os
import numpy as np
import faiss
from typing import TypedDict, List
from langgraph.graph import StateGraph, END

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from sentence_transformers import SentenceTransformer

from app.ai.symptom_search import find_closest_symptom
from app.database.connection import get_db_connection
from app.services.insurance_service import apply_discount
from app.config.config import Config

class AgentState(TypedDict):

    phrases: List[str]

    normalized_symptoms: List[str]

    specialists: List[str]

    recommended_specialists: List[str]

    doctors: List[dict]

    insurance_discount: float

model = SentenceTransformer("all-MiniLM-L6-v2")

symptom_terms = [
    "fever",
    "headache",
    "chest pain",
    "shortness of breath",
    "cough",
    "skin rash",
    "abdominal pain"
]

embeddings = model.encode(symptom_terms)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings))

llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.2,
    openai_api_key=Config.OPENAI_API_KEY
)

def normalize_agent(state: AgentState) -> AgentState:

    phrases = state["phrases"]

    normalized = []

    for phrase in phrases:

        emb =  model.encode([phrase])

        D, I = index.search(np.array(emb), 1)

        symptom = symptom_terms[I[0][0]]

        normalized.append(symptom)

    return {"normalized_symptoms": normalized}


def specialist_lookup_agent(state: AgentState) -> AgentState:

    symptoms = state["normalized_symptoms"]

    conn = get_db_connection()

    cur = conn.cursor()

    try:

        cur.execute(
            "SELECT * FROM sp_get_specialists(%s)",
            (symptoms,)
        )

        specialists = [row[0] for row in cur.fetchall()]

    except Exception:

        specialists = []

    finally:

        cur.close()

        conn.close()

    return {"specialists": specialists}

def recommend_specialists_agent(state: AgentState) -> AgentState:

    symptoms = state["normalized_symptoms"]

    specialists = state["specialists"]

    if not specialists:

        return {"recommended_specialists": []}

    prompt = f"""
    Patient symptoms: {', '.join(symptoms)}

    Available specialists: {', '.join(specialists)}

    Which 1 or 2 specialists should the patient consult first?

    Return comma separated names.
    """

    messages = [
        SystemMessage(content="You are a medical triage assistant."),
        HumanMessage(content=prompt)
    ]

    response = llm.invoke(messages)

    recommended = [
        s.strip()
        for s in response.content.split(",")
        if s.strip() in specialists
    ]

    return {"recommended_specialists": recommended}

def doctor_fetch_agent(state: AgentState) -> AgentState:

    specialists = state["recommended_specialists"]

    if not specialists:

        return {"doctors": []}

    conn = get_db_connection()

    cur = conn.cursor()

    doctors = []

    try:

        cur.execute(
            "SELECT * FROM sp_get_doctors_by_specialists(%s)",
            (specialists,)
        )

        rows = cur.fetchall()

        for row in rows:

            doctors.append({
                "doctor_id": row[0],
                "name": row[1],
                "specialization": row[2],
                "rating": float(row[3]),
                "fees": int(row[4]),
                "hospital": row[5],
                "next_available_date": str(row[6]),
                "start_time": str(row[7]),
                "end_time": str(row[8]),
                "slot_id": row[9]
            })

    except Exception:

        doctors = []

    finally:

        cur.close()

        conn.close()

    return {"doctors": doctors}

def insurance_agent(state: AgentState) -> AgentState:

    doctors = state["doctors"]

    discount = 0.2

    for doc in doctors:

        doc["discounted_fee"] = int(doc["fees"] * (1 - discount))

    return {
        "doctors": doctors,
        "insurance_discount": discount
    }

def build_graph():

    builder = StateGraph(AgentState)

    builder.add_node("normalize", normalize_agent)

    builder.add_node("lookup", specialist_lookup_agent)

    builder.add_node("recommend", recommend_specialists_agent)

    builder.add_node("fetch_doctors", doctor_fetch_agent)

    builder.add_node("insurance", insurance_agent)

    builder.set_entry_point("normalize")

    builder.add_edge("normalize", "lookup")

    builder.add_edge("lookup", "recommend")

    builder.add_edge("recommend", "fetch_doctors")

    builder.add_edge("fetch_doctors", "insurance")

    builder.add_edge("insurance", END)

    return builder.compile()