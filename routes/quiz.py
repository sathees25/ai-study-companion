from fastapi import APIRouter
from pydantic import BaseModel
from services.llm_service import get_response
import json

router = APIRouter()

class QuizRequest(BaseModel):
    topic : str
    num_questions : int = 5

@router.post("/quiz")
async def generate_quiz(req: QuizRequest):
    
    prompt = f"""
    Create {req.num_questions} multiple choice questions on {req.topic}.

    Return the response in JSON format.

    Strict rules:
    - Output must be valid JSON
    - No explanation
    - No extra text

    Format:
    {{
    "quiz": [
        {{
        "question": "...",
        "options": ["A", "B", "C", "D"],
        "answer": "A"
        }}
    ]
    }}
    """
    response = get_response(prompt)

    try:
        quiz_data = json.loads(response)
        return {"quiz": quiz_data}
    except:
        return {
            "error": "Invalid JSON from model",
            "raw_output": response
        }