from fastapi import APIRouter
from pydantic import BaseModel
from services.llm_service import get_response
import json

router = APIRouter()

class FlashCardRequest(BaseModel):
    topic : str
    num_cards : int = 5

@router.post("/flashcard")
async def generate_flashcards(req:FlashCardRequest):
    prompt = f"""
    Create {req.num_cards} flashcards on {req.topic}.

    Return the response in JSON format.

    Strict rules:
    - Output must be valid JSON
    - No explanation
    - No extra text

    Format:
    {{
    "cards": [
        {{
        "question": "...",
        "answer": "..."
        }}
    ]
    }}
    """

    cards = get_response(prompt)
    
    try:
        cards_data = json.loads(cards)
        return {"cards": cards_data}
    except:
        return {
            "error": "Invalid JSON from model",
            "raw_output": cards
        }
