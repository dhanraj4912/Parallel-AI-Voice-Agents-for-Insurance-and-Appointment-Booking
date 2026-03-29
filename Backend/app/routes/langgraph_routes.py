from fastapi import APIRouter,Request
from app.ai.langgraph_agents import build_graph

router = APIRouter()

@router.post("/run_langgraph")

async def run_langgraph(request:Request):

    data = await request.json()

    phrases = data.get("phrases",[])

    graph = build_graph()

    result = graph.invoke({"phrases":phrases})

    return result