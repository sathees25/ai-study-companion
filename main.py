from fastapi import FastAPI
from routes import chat,notes,flashcard,quiz

app = FastAPI()

app.include_router(chat.router)
app.include_router(notes.router)
app.include_router(flashcard.router)
app.include_router(quiz.router)