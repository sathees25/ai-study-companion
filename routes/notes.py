from fastapi import APIRouter
from pydantic import BaseModel
from services.llm_service import get_response
import json

router = APIRouter()

class NotesRequest(BaseModel):
    topic : str

@router.post("/notes")
async def generate_notes(req : NotesRequest):
    prompt = f"""
    Explain {req.topic} in simple notes.
    Use:
    - bullet points
    - examples
    - easy language
    """

    notes = get_response(prompt)
    return {"notes":notes}
