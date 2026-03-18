from fastapi import APIRouter
from pydantic import BaseModel
from services.llm_service import get_response

router = APIRouter()

class ChatRequest(BaseModel):
    question : str

@router.post("/chat")
async def chat(req:ChatRequest):
    answer = get_response(req.question)
    return {'answer' : answer}
